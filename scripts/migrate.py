import re
import sys
import os
import pandas as pd
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import scripts.db as db


def parse_csv_dividends(csv_path: str):
    dividends = []
    with open(csv_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            if line.startswith("Dividends,Data"):
                parts = line.strip().split(",")
                if len(parts) >= 5:
                    currency = parts[2]
                    date = parts[3]
                    description = parts[4]
                    amount = float(parts[5]) if parts[5] else 0.0
                    
                    symbol = parse_symbol(description)
                    
                    dividends.append({
                        "date": date,
                        "symbol": symbol,
                        "amount": amount
                    })
    return dividends


def parse_symbol(description: str):
    match = re.search(r'([A-Z]+)\(', description)
    if match:
        return match.group(1)
    return "UNKNOWN"


def migrate_csv(csv_path: str):
    db.init_db()
    
    dividends = parse_csv_dividends(csv_path)
    print(f"Found {len(dividends)} dividends in CSV")
    
    inserted = db.insert_dividends_batch(dividends, source="csv")
    print(f"Inserted {inserted} new dividends (skipped duplicates)")


def main():
    csv_path = "/home/magoulet/nextcloud/finances/bank_statements/ibkr/dividends_since_opening_accounts_2026-02-11.csv"
    
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        print("Usage: python migrate.py [path_to_csv]")
        sys.exit(1)
    
    migrate_csv(csv_path)
    
    print("\nCurrent dividends in DB:")
    for row in db.get_all_dividends():
        print(f"  {row['date']} | {row['symbol']} | ${row['amount']:.2f} | {row['source']}")


if __name__ == "__main__":
    main()
