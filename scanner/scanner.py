# scanner/scanner.py
import os
import io
import logging
import yfinance as yf
import matplotlib.pyplot as plt
import base64
from scanner.fetch_data import get_data, get_index_symbol
from scanner.mars_calculator import calculate_mars
from scanner.telegram_bot import send_telegram_message_with_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def plot_mars_chart(data, stock):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['MARS'], label='MARS', color='blue')
    plt.plot(data.index, data['Close'], label='Close Price', color='black')
    plt.axhline(0, linestyle='--', color='grey')

    # Add emojis for crossover signals
    for i in range(1, len(data)):
        if data['MARS'].iloc[i-1] < 0 and data['MARS'].iloc[i] > 0:
            plt.plot(data.index[i], data['MARS'].iloc[i], 'g^', markersize=12, label='Buy ✅')
        elif data['MARS'].iloc[i-1] > 0 and data['MARS'].iloc[i] < 0:
            plt.plot(data.index[i], data['MARS'].iloc[i], 'rv', markersize=12, label='Sell 🚨')

    plt.title(f"MARS Signal for {stock}")
    plt.legend()
    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return buffer

def run():
    index_symbol = get_index_symbol()
    stocks = index_symbol[:20]  # Take top 20 for speed

    mars_buy = []
    mars_sell = []

    for stock in stocks:
        logger.info(f"Processing {stock}")
        try:
            data = get_data(stock, index_symbol)
            data = calculate_mars(data)

            latest_mars = data['MARS'].iloc[-1]
            previous_mars = data['MARS'].iloc[-2]

            if previous_mars < 0 < latest_mars or 0 <= latest_mars <= 2:
                mars_buy.append(stock)
                chart = plot_mars_chart(data, stock)
                send_telegram_message_with_image(f"MARS BUY Signal ✅ for {stock}", chart)

            elif previous_mars > 0 > latest_mars or -2 <= latest_mars <= 0:
                mars_sell.append(stock)
                chart = plot_mars_chart(data, stock)
                send_telegram_message_with_image(f"MARS SELL Signal 🚨 for {stock}", chart)

        except Exception as e:
            logger.error(f"Error processing {stock}: {e}")

    if not mars_buy and not mars_sell:
        send_telegram_message_with_image("🛰️ No MARS signals detected today.")

if __name__ == "__main__":
    run()
