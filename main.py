import io
import os
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
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='M')).agg({'Amount': 'sum'})
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
        self.monthly_dividends = df.groupby(pd.Grouper(key='Date', freq='M')).agg({'Amount': 'sum'})

        return self.monthly_dividends


def main():
    CI_BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/ci_direct_investing/'
    CI_FILENAME = 'CI Direct Investing Activity - All time as of Apr 15 2023 - RRSP 103033791.csv'
    ci_path = os.path.join(CI_BASEDIR, CI_FILENAME)
    IBKR_BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/ibkr/'
    IBKR_FILENAME = 'dividends_since_opening_accounts_2023-04-16.csv'
    ibkr_path = os.path.join(IBKR_BASEDIR, IBKR_FILENAME)

    ci_direct = ci_direct_investing()
    ci_direct.parse(ci_path)

    df1 = ci_direct.monthly_dividends()
    print('\nCI Direct Dividends:')
    print(df1)

    print('\nCI Direct Orders (last 10:')
    print(ci_direct.orders().tail(10))

    ibkr = interactive_brokers()
    ibkr.parse(ibkr_path)

    df2 = ibkr.monthly_dividends()
    print('\nInteractive Brokers Dividends:')
    print(df2)


    # Merge dataframes and sum up Amounts
    dfTotal = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    dfTotal['Amount'] = dfTotal.sum(axis=1)
    print('\nCombined Dividends (last 12 months):')
    print(dfTotal.Amount.tail(12))


    # print('{:%Y-%m-%d},{},TSE:{},{},{},${:.2f},{:d},{}.TO'.format(
    #     index, row.Activity, row.Symbol,
    # row.Quantity, row.Price, 0,
    # 1, row.Symbol))

if __name__ == '__main__':
    main()
