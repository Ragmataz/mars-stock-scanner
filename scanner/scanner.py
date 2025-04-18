### ✅ scanner/scanner.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import logging

from scanner.fetch_data import get_data, get_nse500_list, get_index_symbol
from scanner.mars_calculator import calculate_mars
from scanner.telegram_bot import send_telegram_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_chart(data, symbol):
    plt.figure(figsize=(10, 5))
    plt.plot(data['Close'], label='Close', color='black')
    plt.plot(data['MARS'], label='MARS', color='orange')
    plt.axhline(0, linestyle='--', color='gray')

    # Buy signals
    buy_signals = (data['MARS'] > 0) & (data['MARS'].shift(1) <= 0)
    sell_signals = (data['MARS'] < 0) & (data['MARS'].shift(1) >= 0)

    plt.plot(data[buy_signals].index, data[buy_signals]['Close'], '^', color='green', label='BUY ✅')
    plt.plot(data[sell_signals].index, data[sell_signals]['Close'], 'v', color='red', label='SELL 🚨')

    plt.title(f"{symbol} - MARS Indicator")
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    image_bytes = base64.b64encode(buf.read()).decode('utf-8')
    return image_bytes

def run():
    symbols = get_nse500_list()
    index_symbol = get_index_symbol()

    mars_buy = []
    mars_sell = []

    for symbol in symbols:
        logger.info(f"Processing {symbol}")
        try:
            data = get_data(symbol, index_symbol)
            if data is None or data.empty:
                continue

            data = calculate_mars(data)

            # Extended signal range
            latest_mars = data['MARS'].iloc[-1]

            if 0 < latest_mars < 2:
                chart = generate_chart(data, symbol)
                mars_buy.append((symbol, chart))

            elif -2 < latest_mars < 0:
                chart = generate_chart(data, symbol)
                mars_sell.append((symbol, chart))

        except Exception as e:
            logger.error(f"Error processing {symbol}: {e}")

    if mars_buy or mars_sell:
        message = "📈 *MARS Signals*\n\n"
        if mars_buy:
            message += "✅ *Buy Signals*:\n"
            for symbol, chart in mars_buy:
                send_telegram_message(f"✅ BUY Signal for *{symbol}*", chart)

        if mars_sell:
            message += "🚨 *Sell Signals*:\n"
            for symbol, chart in mars_sell:
                send_telegram_message(f"🚨 SELL Signal for *{symbol}*", chart)
    else:
        send_telegram_message("📭 No MARS signals today.")

if __name__ == "__main__":
    run()
