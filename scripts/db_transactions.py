import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_mysql_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database="portfolio"
    )


def transaction_exists(date: str, ticker: str, units: float, price: float) -> bool:
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM transactions WHERE Date = %s AND Ticker = %s AND Units = %s AND Price = %s",
        (date, ticker, units, price)
    )
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def insert_transaction(date: str, type_: str, ticker: str, units: float, price: float, fees: float = None):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO transactions (Date, Type, Ticker, Units, Price, Fees, Broker, Currency)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (date, type_, ticker, units, price, fees, "IBKR", "USD")
    )
    conn.commit()
    conn.close()


def insert_contribution(date: str, amount: float, notes: str = None):
    conn = get_mysql_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO contributions (date, contribution, broker, currency, notes)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (date, amount, "IBKR", "USD", notes)
    )
    conn.commit()
    conn.close()
