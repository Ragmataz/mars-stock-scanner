import yfinance as yf
import pandas as pd

def get_nse500_list():
    return ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]  # Sample list

def get_index_symbol():
    return "^NSEI"

def get_data(symbol, index_symbol):
    try:
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        if data.empty:
            return None

        data["Symbol"] = symbol
        data.dropna(inplace=True)
        return data
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None
