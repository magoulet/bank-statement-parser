import io
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import pandas as pd
import scripts.db as db


class ci_direct_investing():
    def __init__(self):
        pass

    def print(self):
        print(f"Transactions: {self.transactions}")

    def parse(self, path):
        df = pd.read_csv(path,
                         # index_col=['Effective Date'],
                         parse_dates=['Effective Date']
                         )
        df = df.rename(columns={'Effective Date': 'Date', 'Total Value': 'Amount'})
        self.transactions = df

    def dividends(self):
        df = self.transactions
        condition = df['Activity'] == 'Dividend'
        cols = ['Date', 'Description', 'Amount']
        self.dividends = df.loc[condition, cols]

        return self.dividends

    def monthly_dividends(self):
        self.dividends()
        df = self.dividends
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='ME')).agg({'Amount': 'sum'})
        # print(f"Dividend summary: \n{self.monthly_dividends}")
        return self.monthly_dividends

    def orders(self):
        df = self.transactions
        condition = (df['Activity'] == 'Buy') | (df['Activity'] == 'Sell')
        cols = ['Date', 'Activity', 'Symbol','Quantity','Price', 'Amount']
        self.orders = df.loc[condition, cols]

        return self.orders

class interactive_brokers():
    def __init__(self):
        pass

    def print(self):
        print(f"Transactions: {self.transactions}")

    def parse(self, path):
        buf = io.StringIO()

        with open(path, "r") as f:
            lines = f.readlines()
        with buf as f:
            headerFlag = False
            for line in lines:
                if (line.startswith("Dividends,Header")) and not headerFlag :
                    f.write(line)
                    headerFlag = True
                if line.startswith("Dividends,Data,USD"):
                    f.write(line)

            buf.seek(0)
            df = pd.read_csv(buf,
                             # index_col=['Effective Date'],
                             parse_dates=['Date']
                             )
        self.transactions = df

    def dividends(self):
        df = self.transactions
        self.dividends = df

        return self.dividends

    def monthly_dividends(self):
        self.dividends()
        df = self.dividends
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='ME')).agg({'Amount': 'sum'})

        return self.monthly_dividends

    def dividends_from_db(self):
        rows = db.get_all_dividends()
        data = [(r['date'], r['symbol'], r['amount']) for r in rows]
        df = pd.DataFrame(data, columns=['Date', 'Symbol', 'Amount'])
        df['Date'] = pd.to_datetime(df['Date'])
        return df

    def monthly_dividends_from_db(self):
        df = self.dividends_from_db()
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='ME')).agg({'Amount': 'sum'})
        return self.monthly_dividends

class closed_accounts():
    def __init__(self):
        pass

    def print(self):
        pass

    def parse(self, path):
        df = pd.read_csv(path,
                 # index_col=['Effective Date'],
                 parse_dates=['Date']
                 )
        self.transactions = df

    def dividends(self):
        self.dividends = self.transactions
        return self.dividends

    def monthly_dividends(self):
        self.dividends()
        df = self.dividends
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='ME')).agg({'Amount': 'sum'})
        return self.monthly_dividends
