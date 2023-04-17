# ToDo:
# * use config file (yml)
# * modularize the main logic
# * run a single df and each account is an extra column (join operation)

import io
import matplotlib.pyplot as plt
import os
import pandas as pd

from classes import *

def plot_dividends(df):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df['Amount'], marker='o')
    # ax.stackplot(results['periodEnd'], results['PPT']/8, results['Sick']/8, results['Vac']/8)
    # ax.stackplot(results['periodEnd'], results['sickLost'], results['vacLost'], colors=['red', 'blue'])
    ax.set(title='Dividend Amount',
           ylabel='Amount',
           xlabel='Period End Date')
    # ax.legend(['PTO', 'PPT', 'Sick', 'Vac', 'Lost (PPT)','Lost (Vac)'], loc='best')
    plt.show()


def main():
    CI_BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/ci_direct_investing/'
    IBKR_BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/ibkr/'
    CLOSED_ACCOUNTS_BASEDIR = '/home/magoulet/gdrive/finances/bank_statements/'

    CI_FILENAME = 'CI Direct Investing Activity - All time as of Apr 15 2023 - RRSP 103033791.csv'
    IBKR_FILENAME = 'dividends_since_opening_accounts_2023-04-16.csv'
    CLOSED_ACCOUNTS_FILENAME = 'Dividend Gains - pre_2022-04-30.csv'

    ci_path = os.path.join(CI_BASEDIR, CI_FILENAME)
    ibkr_path = os.path.join(IBKR_BASEDIR, IBKR_FILENAME)
    closed_accounts_path = os.path.join(CLOSED_ACCOUNTS_BASEDIR, CLOSED_ACCOUNTS_FILENAME)

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

    other = closed_accounts()
    other.parse(closed_accounts_path)
    df3 = other.monthly_dividends()
    print(df3)


    # Merge dataframes and sum up Amounts
    dfTotal = pd.merge(df1, df2, how='outer', left_index=True, right_index=True)
    dfTotal = pd.merge(dfTotal, df3, how='outer', left_index=True, right_index=True)
    dfTotal['Amount'] = dfTotal.sum(axis=1)
    print('\nCombined Dividends (last 12 months):')
    print(dfTotal.Amount.tail(12))

    plot_dividends(dfTotal.groupby(pd.Grouper(freq='Y')).agg({'Amount': 'sum'}))


    # print('{:%Y-%m-%d},{},TSE:{},{},{},${:.2f},{:d},{}.TO'.format(
    #     index, row.Activity, row.Symbol,
    # row.Quantity, row.Price, 0,
    # 1, row.Symbol))

if __name__ == '__main__':
    main()
