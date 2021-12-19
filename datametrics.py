# method library
import pandas as pd


def pct_daily_returns(data):
    return (data.iloc[1:] / data.iloc[:-1].values) - 1


def rolling_avg(data, period):
    rolling_windows = data.rolling(period, min_periods=1)
    return rolling_windows.mean()

def