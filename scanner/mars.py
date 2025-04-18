# scanner/mars.py

import pandas as pd

def moving_average(series, length, ma_type="SMA"):
    if ma_type == "EMA":
        return series.ewm(span=length).mean()
    elif ma_type == "WMA":
        weights = range(1, length + 1)
        return series.rolling(length).apply(lambda prices: sum(prices * weights)/sum(weights), raw=True)
    else:
        return series.rolling(length).mean()

def compute_mars(stock_df, index_df, ma_type="SMA", ma_len=50):
    ma_stock = moving_average(stock_df["Close"], ma_len, ma_type)
    ma_index = moving_average(index_df["Close"], ma_len, ma_type)

    symbol_percent = (stock_df["Close"] - ma_stock) / ma_stock * 100
    index_percent = (index_df["Close"] - ma_index) / ma_index * 100

    val = symbol_percent - index_percent
    return val
