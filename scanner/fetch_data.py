# scanner/fetch_data.py

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_data(ticker, period="6mo", interval="1d"):
    data = yf.download(ticker, period=period, interval=interval, progress=False)
    data.dropna(inplace=True)
    return data

def get_nse500_list():
    url = "https://archives.nseindia.com/content/indices/ind_nifty500list.csv"
    return pd.read_csv(url)["Symbol"].tolist()

def get_index_symbol(index="CNX500"):
    return {
        "CNX500": "^CRSLDX",
        "NIFTY": "^NSEI",
        "MIDCAP150": "^CNXMIDCAP",
        "SMALLCAP": "^CNXSMCP"
    }.get(index.upper(), "^CRSLDX")
