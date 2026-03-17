import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

import scripts.db as db
import scripts.db_transactions as db_transactions


def main():
    # Get trades from SQLite (both flex and intraday sources)
    print("Reading trades from local database...")
    trades = db.get_trades_by_source(['flex', 'intraday'])
    print(f"Found {len(trades)} trades in SQLite")
    
    new_trades = []
    for t in trades:
        # Convert sqlite3.Row to dict
        trade = {
            "trade_date": t["trade_date"],
            "symbol": t["symbol"],
            "units": t["quantity"],
            "price": t["trade_price"]
        }
        
        if db_transactions.transaction_exists(trade["trade_date"], trade["symbol"], trade["units"], trade["price"]):
            print(f"  Skip: {trade['trade_date']} {trade['symbol']} {trade['units']} (already in MySQL)")
            continue
        
        # Determine Buy/Sell from quantity
        units_val = float(trade["units"])
        type_ = "Sell" if units_val < 0 else "Buy"
        # Keep negative for Sell, positive for Buy
        units = units_val
        
        db_transactions.insert_transaction(
            date=trade["trade_date"],
            type_=type_,
            ticker=trade["symbol"],
            units=units,
            price=trade["price"],
            fees=None
        )
        new_trades.append(trade)
        print(f"  Inserted: {trade['trade_date']} {type_} {units} {trade['symbol']} @ ${trade['price']}")
    
    if new_trades:
        print(f"\n🔔 Inserted {len(new_trades)} new transactions to MySQL")
    else:
        print(f"\n✅ No new transactions (all up to date)")
    
    # Once all transactions are inserted, prompt for cash contribution
    if new_trades:
        response = input("\nRecord cash contribution for these transactions? (y/n): ").strip().lower()
        if response == "y":
            amount_input = input("  Enter amount (xxx.xx): ").strip()
            try:
                amount = float(amount_input)
                notes_input = input("  Notes (optional, press Enter to skip): ").strip()
                notes = notes_input if notes_input else None
                # Use the date of the most recent trade
                db_transactions.insert_contribution(new_trades[0]["trade_date"], amount, notes)
                print(f"  Contribution of ${amount} recorded")
            except ValueError:
                print("  Invalid amount, skipping contribution")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
