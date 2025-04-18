import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from scanner.config import NSE_500_TICKERS, INDEX_TICKER

def get_nse500_list():
    return NSE_500_TICKERS

def get_index_symbol():
    return INDEX_TICKER

def get_data(stock_list, index_symbol):
    end = datetime.now()
    start = end - timedelta(days=365)

    all_data = {}
    for symbol in stock_list + [index_symbol]:
        df = yf.download(symbol + ".NS", start=start, end=end, progress=False)
        all_data[symbol] = df
    return all_data
