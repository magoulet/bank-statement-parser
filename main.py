import datetime as dt
import os
import numpy as np
import pandas as pd

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
        self.transactions = df

    def dividends(self):
        df = self.transactions
        condition = df['Activity'] == 'Dividend'
        cols = ['Effective Date', 'Description', 'Total Value']
        self.dividends = df.loc[condition, cols]

        # print(f"Last 5 dividend entries: \n{self.dividends.tail(5)}")

        return self.dividends

    def monthly_dividends(self):
        self.dividends()
        df = self.dividends
        self.monthly_dividends = df.groupby(pd.Grouper(key='Effective Date', freq='M')).agg({'Total Value': 'sum'})
        self.dividends.tail(5)
        # print(f"Dividend summary: \n{self.monthly_dividends}")
        return self.monthly_dividends
class ibkr():
    def __init__(self):
        pass

    def print(self):
        print(f"Transactions: {self.transactions}")

    def parse(self, path):
        df = pd.read_csv(path,
                         # index_col=['Effective Date'],
                         parse_dates=['Effective Date']
                         )
        self.transactions = df

    def dividends(self):
        df = self.transactions
        condition = df['Activity'] == 'Dividend'
        cols = ['Effective Date', 'Description', 'Total Value']
        self.dividends = df.loc[condition, cols]

        # print(f"Last 5 dividend entries: \n{self.dividends.tail(5)}")

        return self.dividends

    def monthly_dividends(self):
        self.dividends()
        df = self.dividends
        self.monthly_dividends = df.groupby(pd.Grouper(key='Effective Date', freq='M')).agg({'Total Value': 'sum'})
        self.dividends.tail(5)
        # print(f"Dividend summary: \n{self.monthly_dividends}")
        return self.monthly_dividends


def main():
    BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/ci_direct_investing/'
    FILENAME = 'CI Direct Investing Activity - All time as of Apr 15 2023 - RRSP 103033791.csv'
    path = os.path.join(BASEDIR, FILENAME)

    ci_direct = ci_direct_investing()
    ci_direct.parse(path)

    df = ci_direct.monthly_dividends()

    print(df)

if __name__ == '__main__':
    main()
