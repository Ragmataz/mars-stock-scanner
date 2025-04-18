import logging
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

from scanner.telegram_bot import send_telegram_message, send_telegram_message_with_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define your list of symbols
SYMBOLS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS"
]

def calculate_mars(data):
    try:
        data['EMA_5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA_20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['MARS'] = data['EMA_5'] - data['EMA_20']
        return data
    except Exception as e:
        logger.error(f"Error in MARS calculation: {e}")
        return None

def plot_stock_chart(data, symbol):
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(data['Close'], label='Close Price', color='black')
        plt.plot(data['EMA_5'], label='EMA 5', linestyle='--', color='blue')
        plt.plot(data['EMA_20'], label='EMA 20', linestyle='--', color='orange')
        plt.title(f'{symbol} Price Chart with MARS')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        chart_filename = f"{symbol.replace('.', '_')}_chart.png"
        plt.savefig(chart_filename)
        plt.close()
        return chart_filename
    except Exception as e:
        logger.error(f"Error generating chart for {symbol}: {e}")
        return None

def analyze_symbol(symbol):
    try:
        logger.info(f"Processing {symbol}")
        end = datetime.today()
        start = end - timedelta(days=180)
        df = yf.download(symbol, start=start, end=end, auto_adjust=True)

        if df is None or df.empty:
            raise ValueError("Downloaded data is empty or None")

        df = calculate_mars(df)

        if df is None or df.empty:
            raise ValueError("Failed to calculate MARS")

        if df['MARS'].iloc[-1] > 0 and df['MARS'].iloc[-2] <= 0:
            logger.info(f"MARS signal detected for {symbol}")
            chart_path = plot_stock_chart(df, symbol)
            if chart_path:
                send_telegram_message_with_image(f"MARS signal detected for {symbol}", chart_path)
            return True

    except Exception as e:
        logger.error(f"Error processing {symbol}: {e}")

    return False

def run():
    signals_found = False

    for symbol in SYMBOLS:
        if analyze_symbol(symbol):
            signals_found = True

    if not signals_found:
        send_telegram_message("🛰️ No MARS signals detected today.")

if __name__ == "__main__":
    run()
