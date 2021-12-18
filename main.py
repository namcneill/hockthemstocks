from pprintpp import pprint
import pandas as pd


def ticker_to_path(data_path, ticker):
    return data_path + ticker + '.csv'


def get_data(data_path, tickers, date_range):
    df_final = pd.DataFrame(index=date_range)
    if 'SPY' not in tickers:
        tickers.insert(0, 'SPY')
    for ticker in tickers:
        ticker_path = ticker_to_path(data_path, ticker)

        df_temp = pd.read_csv(ticker_path, index_col='Date', parse_dates=True, usecols=['Date', 'Adj Close'], na_values=['nan'])
        df_temp = df_temp.rename(columns={'Adj Close': ticker})
        df_final = df_final.join(df_temp)
        if ticker == 'SPY':
            df_final = df_final.dropna(subset=['SPY'])

    return df_final


def main():
    data_dir = 'stockdata\\'
    tickers = ['AAPL', 'GOOG', 'MSFT']
    start_date = '2010-01-01'
    end_date = '2021-12-12'
    date_range = pd.date_range(start_date, end_date)
    df_data = get_data(data_dir, tickers, date_range)
    pprint(df_data)


if __name__ == '__main__':
    main()
