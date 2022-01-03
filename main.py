import pandas as pd
import matplotlib.pyplot as plt
import datametrics as dm


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
    start_date = '2021-01-01'
    end_date = '2021-12-12'

    data_metrics = dm.DataMetrics(data_dir=data_dir, tickers=tickers, start_date=start_date, end_date=end_date)

    # data_metrics.plot_metrics('MSFT')
    # print(data_metrics.multi_poly(50))

    plot_data(data_metrics.multi_poly(50), "Time", "Concavity", "Concavity")


if __name__ == '__main__':
    main()
