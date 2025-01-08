import matplotlib.pyplot as plt

from classes import *


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

    config = AppConfig()

    ###########
    # CI Direct
    ###########
    ci_direct = ci_direct_investing()
    ci_direct.parse(config.get_ci_path())

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
    ibkr.parse(config.get_ibkr_path())

    df = ibkr.monthly_dividends()
    df.rename(columns={'Amount': 'Amount_IBKR'}, inplace=True)
    total = pd.concat([total, df], axis=1)
    # print('\nInteractive Brokers Dividends:')
    # print(df)

    ###########
    # Closed Accounts
    ###########
    closed = closed_accounts()
    closed.parse(config.get_closed_path())
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

    plot_dividends(total.groupby(pd.Grouper(freq='YE')).sum())
    
    # plot_dividends(total.groupby(pd.Grouper(freq='Y')).agg({'TotalAmount': 'sum'}))


if __name__ == '__main__':
    main()
