import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import xml.etree.ElementTree as ET
import requests
import time
from dotenv import load_dotenv

load_dotenv()

import db

FLEX_TOKEN = os.environ.get("IBKR_FLEX_TOKEN")
FLEX_QUERY_ID = os.environ.get("IBKR_FLEX_QUERY_ID")

BASE_URL = "https://ndcdyn.interactivebrokers.com/AccountManagement/FlexWebService"


def send_request(token: str, query_id: str) -> str:
    url = f"{BASE_URL}/SendRequest"
    params = {"t": token, "q": query_id, "v": 3}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    
    root = ET.fromstring(resp.text)
    status = root.find("Status").text
    
    if status != "Success":
        raise Exception(f"Request failed: {root.find('ErrorMessage').text if root.find('ErrorMessage') is not None else 'Unknown error'}")
    
    ref_code = root.find("ReferenceCode").text
    return ref_code


def get_statement(token: str, ref_code: str) -> str:
    url = f"{BASE_URL}/GetStatement"
    params = {"t": token, "q": ref_code, "v": 3}
    resp = requests.get(url, params=params, allow_redirects=True)
    resp.raise_for_status()
    return resp.text


def parse_flex_xml(xml_content: str):
    root = ET.fromstring(xml_content)
    trades = []
    dividends = []
    
    for stmt in root.findall(".//FlexStatement"):
        for trade in stmt.findall(".//Trade"):
            trades.append({
                "trade_date": trade.get("tradeDate"),
                "symbol": trade.get("symbol"),
                "description": trade.get("description"),
                "quantity": trade.get("quantity"),
                "trade_price": float(trade.get("tradePrice")),
                "proceeds": float(trade.get("proceeds"))
            })
        
        for cash_tx in stmt.findall(".//CashTransaction"):
            if cash_tx.get("type") == "Dividends":
                date_time = cash_tx.get("dateTime")
                date = date_time.split(";")[0] if ";" in date_time else date_time
                dividends.append({
                    "date": date,
                    "symbol": cash_tx.get("symbol"),
                    "amount": float(cash_tx.get("amount"))
                })
    
    return trades, dividends


def sync_from_flex():
    if not FLEX_TOKEN or not FLEX_QUERY_ID:
        print("Please set IBKR_FLEX_TOKEN and IBKR_FLEX_QUERY_ID in .env")
        sys.exit(1)
    
    print("Fetching flex report...")
    ref_code = send_request(FLEX_TOKEN, FLEX_QUERY_ID)
    time.sleep(2)
    xml = get_statement(FLEX_TOKEN, ref_code)
    
    trades, dividends = parse_flex_xml(xml)
    
    print(f"Found {len(trades)} trades and {len(dividends)} dividends")
    
    trades_inserted = db.insert_trades_batch(trades, source="flex")
    dividends_inserted = db.insert_dividends_batch(dividends, source="flex")
    
    print(f"Inserted {trades_inserted} new trades, {dividends_inserted} new dividends")
    
    return trades, dividends


def main():
    db.init_db()
    
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        sync_from_flex()
    else:
        print("Usage: python flex_sync.py sync")
        print("\nOr import and call sync_from_flex() directly")


if __name__ == "__main__":
    main()
