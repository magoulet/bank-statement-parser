import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

from classes import *
import scripts.db as db

CI_BASEDIR = os.environ.get("CI_BASEDIR", "")
CI_FILENAME = os.environ.get("CI_FILENAME", "")
CLOSED_BASEDIR = os.environ.get("CLOSED_BASEDIR", "")
CLOSED_FILENAME = os.environ.get("CLOSED_FILENAME", "")


def plot_dividends(df):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(df['TotalAmount'], marker='o')
    # ax.stackplot(df.index, df['Amount_CIDirect'], df['Amount_IBKR'], df['Amount_Closed'])
    ax.set(title='Dividend Amount',
           ylabel='Amount',
           xlabel='Period End Date')
    # ax.legend(['CIDirect', 'IBKR', 'Closed'], loc='upper left')
    plt.show()


def main():
    total = pd.DataFrame()

    ###########
    # CI Direct
    ###########
    ci_direct = ci_direct_investing()
    ci_direct.parse(os.path.join(CI_BASEDIR, CI_FILENAME))

    df = ci_direct.monthly_dividends()
    df.rename(columns={'Amount': 'Amount_CIDirect'}, inplace=True)
    total = pd.concat([total, df], axis=1)
    # print('\nCI Direct Dividends:')
    # print(df)

    # print('\nCI Direct Orders (last 10:')
    # print(ci_direct.orders().tail(10))

    ###########
    # IBKR
    ###########
    ibkr = interactive_brokers()
    db.init_db()

    df = ibkr.monthly_dividends_from_db()
    df.rename(columns={'Amount': 'Amount_IBKR'}, inplace=True)
    total = pd.concat([total, df], axis=1)

    ###########
    # Closed Accounts
    ###########
    closed = closed_accounts()
    closed.parse(os.path.join(CLOSED_BASEDIR, CLOSED_FILENAME))
    df = closed.monthly_dividends()
    df.rename(columns={'Amount': 'Amount_Closed'}, inplace=True)
    total = pd.concat([total, df], axis=1)
    # print('\nClosed Accounts Dividends:')
    # print(df)


    # Merge dataframes and sum up Amounts
    total['TotalAmount'] = total.sum(axis=1)

    # Sort chronologically
    total.sort_index(inplace=True)
    
    print('\nCombined Dividends (last 12 months):')
    print(total.TotalAmount.tail(12))

    print('\nYearly Dividends by Broker:')
    yearly_dividends = total.groupby(pd.Grouper(freq='YE')).sum()
    yearly_summary = yearly_dividends[['Amount_CIDirect', 'Amount_IBKR']]
    yearly_summary.columns = ['CI Direct', 'IBKR']
    print(yearly_summary['2021':].round(2))  # Only show from 2021 onwards

    # Monthly total dividends in a LibreOffice Calc-friendly format
    # This prints two columns: Date (start of month) and Dividend Income (monthly total)
    monthly_total = total['TotalAmount'].groupby(pd.Grouper(freq='ME')).sum()
    monthly_total_df = monthly_total.to_frame(name='Dividend Income')

    # Use the first day of each month to match the spreadsheet style (e.g. 1/1/2012)
    monthly_total_df.index = monthly_total_df.index.to_period('M').to_timestamp('D', how='start')
    monthly_total_df.insert(0, 'Date', monthly_total_df.index.strftime('%-m/%-d/%Y'))

    print('\nMonthly Dividends for Calc (copy-paste the CSV below):')
    # Format numbers to 2 decimal places to avoid long floating-point representations
    print(monthly_total_df.to_csv(index=False, float_format='%.2f'))

    plot_dividends(total.groupby(pd.Grouper(freq='YE')).sum())
    
    # plot_dividends(total.groupby(pd.Grouper(freq='Y')).agg({'TotalAmount': 'sum'}))


if __name__ == '__main__':
    main()
