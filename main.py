from pprintpp import pprint
import pandas as pd
import matplotlib.pyplot as plt
import datametrics as dm
import numpy as np


def ticker_to_path(data_path, ticker):
    return data_path + ticker + '.csv'


def get_data(data_path, tickers, date_range):
    df_final = pd.DataFrame(index=date_range)
    if 'SPY' not in tickers:
        tickers.insert(0, 'SPY')
    for ticker in tickers:
        ticker_path = ticker_to_path(data_path, ticker)

        df_temp = pd.read_csv(ticker_path,
                              index_col='Date',
                              parse_dates=True,
                              usecols=['Date', 'Adj Close'],
                              na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': ticker})
        df_final = df_final.join(df_temp)
        if ticker == 'SPY':
            df_final = df_final.dropna(subset=['SPY'])

    return df_final


def normalize_data(data):
    # index = date, columns = ticker
    return data.iloc[1:] / data.iloc[0]


def plot_data(data, x_label, y_label, title):
    data.plot()
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc='best')
    plt.show()


def main():
    data_dir = 'stockdata\\'
    tickers = ['AAPL', 'GOOG', 'MSFT']
    start_date = '2010-01-01'
    end_date = '2021-12-12'
    date_range = pd.date_range(start_date, end_date)
    df_data = get_data(data_dir, tickers, date_range)
    norm_data = normalize_data(df_data)
    pdr = dm.pct_daily_returns(df_data)
    r_avg = dm.rolling_avg(df_data, 5)
    pprint(r_avg)
    pprint(df_data)
    # pprint(pdr)
    # pprint(norm_data)
    # plot_data(pdr, x_label='Time', y_label='Daily Gains', title='Daily TechStock Growth')
    # plot_data(norm_data, x_label='Time', y_label='Normalized Gains', title='Normalized TechStock Growth')
    # plot_data(df_data, x_label='Time', y_label='Gains', title='TechStock Growth')


if __name__ == '__main__':
    main()