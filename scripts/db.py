import sqlite3
import os
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "ibkr_data.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dividends (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            symbol TEXT NOT NULL,
            amount REAL NOT NULL,
            source TEXT DEFAULT 'flex',
            UNIQUE(date, symbol, amount)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY,
            trade_date TEXT NOT NULL,
            symbol TEXT NOT NULL,
            description TEXT,
            quantity INTEGER NOT NULL,
            trade_price REAL NOT NULL,
            proceeds REAL NOT NULL,
            source TEXT DEFAULT 'flex',
            UNIQUE(trade_date, symbol, quantity, trade_price)
        )
    """)
    conn.commit()
    conn.close()


def insert_dividend(date: str, symbol: str, amount: float, source: str = "flex"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO dividends (date, symbol, amount, source) VALUES (?, ?, ?, ?)",
            (date, symbol, amount, source)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting dividend: {e}")
    finally:
        conn.close()


def insert_dividends_batch(dividends: list, source: str = "flex"):
    conn = get_connection()
    inserted = 0
    try:
        for d in dividends:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO dividends (date, symbol, amount, source) VALUES (?, ?, ?, ?)",
                (d["date"], d["symbol"], d["amount"], source)
            )
            if cursor.rowcount > 0:
                inserted += 1
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting dividends: {e}")
    finally:
        conn.close()
    return inserted


def get_all_dividends():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    df = conn.execute(
        "SELECT date, symbol, amount, source FROM dividends ORDER BY date"
    ).fetchall()
    conn.close()
    return df


def get_dividends_since(date: str):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    df = conn.execute(
        "SELECT date, symbol, amount, source FROM dividends WHERE date >= ? ORDER BY date",
        (date,)
    ).fetchall()
    conn.close()
    return df


def insert_trade(trade_date: str, symbol: str, description: str, quantity: int, trade_price: float, proceeds: float, source: str = "flex"):
    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO trades (trade_date, symbol, description, quantity, trade_price, proceeds, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (trade_date, symbol, description, quantity, trade_price, proceeds, source)
        )
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting trade: {e}")
    finally:
        conn.close()


def insert_trades_batch(trades: list, source: str = "flex"):
    conn = get_connection()
    inserted = 0
    try:
        for t in trades:
            cursor = conn.execute(
                "INSERT OR IGNORE INTO trades (trade_date, symbol, description, quantity, trade_price, proceeds, source) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (t["trade_date"], t["symbol"], t.get("description", ""), t["quantity"], t["trade_price"], t["proceeds"], source)
            )
            if cursor.rowcount > 0:
                inserted += 1
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error inserting trades: {e}")
    finally:
        conn.close()
    return inserted


def get_all_trades():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    df = conn.execute(
        "SELECT trade_date, symbol, description, quantity, trade_price, proceeds, source FROM trades ORDER BY trade_date"
    ).fetchall()
    conn.close()
    return df


def get_trades_by_source(sources: list):
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    placeholders = ','.join(['?'] * len(sources))
    df = conn.execute(
        f"SELECT trade_date, symbol, description, quantity, trade_price, proceeds, source FROM trades WHERE source IN ({placeholders}) ORDER BY trade_date",
        sources
    ).fetchall()
    conn.close()
    return df
