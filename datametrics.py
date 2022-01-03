# method library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass


@dataclass
class DataMetrics:
    data_dir: str
    tickers: list
    start_date: str
    end_date: str
    ra_period: int = 20

    @property
    def date_range(self):
        return pd.date_range(self.start_date, self.end_date)

    @property
    def raw_data(self):
        df_adj_close = pd.DataFrame(index=self.date_range)
        if 'SPY' not in self.tickers:
            self.tickers.insert(0, 'SPY')
        for ticker in self.tickers:
            ticker_path = ticker_to_path(self.data_dir, ticker)

            df_temp = pd.read_csv(ticker_path,
                                  index_col='Date',
                                  parse_dates=True,
                                  usecols=['Date', 'Adj Close'],
                                  na_values=['nan'])
            df_temp = df_temp.rename(columns={'Adj Close': ticker})
            df_adj_close = df_adj_close.join(df_temp)
            if ticker == 'SPY':
                df_adj_close = df_adj_close.dropna(subset=['SPY'])

        return df_adj_close

    @property
    def pct_daily_returns(self):
        return (self.raw_data.iloc[1:] / self.raw_data.iloc[:-1].values) - 1

    @property
    def rolling_avg(self):
        rolling_windows = self.raw_data.rolling(self.ra_period, min_periods=1)
        return rolling_windows.mean()

    @property
    def bollinger_bands(self):
        std = self.raw_data.rolling(self.ra_period, min_periods=1).std()
        boll_up = self.rolling_avg + std * 2
        boll_down = self.rolling_avg - std * 2
        return boll_up, boll_down

    def poly_regression(self, ticker, poly_period):
        concavity = pd.DataFrame(index=self.raw_data.index)
        con_vals = np.array([])

        for window in self.raw_data[ticker].rolling(poly_period, min_periods=poly_period):
            size = len(window.index)
            if size >= poly_period:
                window = (window / window[0])
                x = np.linspace(0, size - 1, size)
                y = window.to_numpy()
                pfit = np.polyfit(x, y, 2)
                con_vals = np.append(con_vals, pfit[0])
            else:
                con_vals = np.append(con_vals, 0.0)

        concavity[ticker] = con_vals.tolist()
        return concavity

    def multi_poly(self, poly_period):
        data_concavity = pd.DataFrame(index=self.raw_data.index)
        for ticker in self.tickers:
            single_poly = self.poly_regression(ticker, poly_period)
            data_concavity = data_concavity.join(single_poly)
        return data_concavity

    def plot_metrics(self, symbol):
        main_plot = self.raw_data[symbol].plot()
        self.rolling_avg[symbol].plot(ax=main_plot)
        bb_up, bb_down = self.bollinger_bands
        bb_up[symbol].plot(ax=main_plot)
        bb_down[symbol].plot(ax=main_plot)
        plt.title('All metrics')
        plt.xlabel('Time')
        plt.ylabel('Adj. Market Close')
        plt.legend(loc='best')
        plt.show()


def ticker_to_path(data_path, ticker):
    return data_path + ticker + '.csv'
