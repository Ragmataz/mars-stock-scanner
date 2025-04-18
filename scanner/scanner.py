import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
import logging
from datetime import datetime
from scanner.mars_calculator import calculate_mars
from scanner.fetch_data import get_nse500_list, get_data
from scanner.telegram_bot import send_telegram_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_plot(data, symbol):
    plt.figure(figsize=(10, 4))
    plt.plot(data['Close'], label='Close Price', color='black')
    plt.plot(data['MARS'], label='MARS', color='orange')
    plt.axhline(0, color='gray', linestyle='--')

    last_mars = data['MARS'].iloc[-1]
    last_close = data['Close'].iloc[-1]

    # Mark the latest point
    if last_mars > last_close:
        plt.scatter(data.index[-1], last_mars, color='green', s=100, label='Buy 🚀')
    elif last_mars < last_close:
        plt.scatter(data.index[-1], last_mars, color='red', s=100, label='Sell 🚨')

    plt.title(f'{symbol} MARS Signal')
    plt.legend()
    plt.tight_layout()

    filename = f"{symbol}_chart.png"
    plt.savefig(filename)
    plt.close()
    return filename

def process_stock(symbol):
    try:
        data = get_data(symbol, index_symbol)
        if data is None or data.empty:
            logger.warning(f"No data for {symbol}")
            return

        data = calculate_mars(data)
        data = data.dropna(subset=['MARS'])

        if data.empty:
            logger.warning(f"No MARS data for {symbol}")
            return

        last_mars = data['MARS'].iloc[-1]
        last_close = data['Close'].iloc[-1]

        if pd.notna(last_mars) and pd.notna(last_close):
            if 0 < last_mars < 2:
                message = f"✅ MARS BUY SIGNAL for {symbol} on {datetime.now().strftime('%Y-%m-%d')}"
                plot_path = generate_plot(data, symbol)
                send_telegram_message(message, plot_path)
            elif -2 < last_mars < 0:
                message = f"🚨 MARS SELL SIGNAL for {symbol} on {datetime.now().strftime('%Y-%m-%d')}"
                plot_path = generate_plot(data, symbol)
                send_telegram_message(message, plot_path)
            else:
                logger.info(f"No MARS crossover signal for {symbol}")
        else:
            logger.warning(f"Skipping {symbol} due to NaN values in MARS or Close")

    except Exception as e:
        logger.error(f"Error processing {symbol}: {e}")

def main():
    stock_list = get_nse500_list()
    signals_found = False

    for symbol in stock_list:
        logger.info(f"Processing {symbol}")
        old_signal_count = len(os.listdir("."))  # Check file count before
        process_stock(symbol)
        new_signal_count = len(os.listdir("."))  # Check after

        if new_signal_count > old_signal_count:
            signals_found = True

    if not signals_found:
        send_telegram_message("😴 No MARS signals today.")

if __name__ == "__main__":
    main()
