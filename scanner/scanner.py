import os
import logging
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
PLOTS_DIR = "plots"

# Ensure plots directory exists
os.makedirs(PLOTS_DIR, exist_ok=True)

def fetch_stock_data(symbol, period="6mo", interval="1d"):
    try:
        data = yf.download(symbol, period=period, interval=interval)
        if data.empty:
            logger.warning(f"No data found for {symbol}")
            return None
        return data
    except Exception as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None

def calculate_mars(data):
    try:
        data['MARS'] = data['Close'].rolling(window=14).mean()  # Placeholder for actual MARS calculation
        return data
    except Exception as e:
        logger.error(f"Error calculating MARS: {e}")
        return data

def generate_plot(data, symbol):
    try:
        plt.figure(figsize=(10, 5))
        plt.plot(data.index, data['Close'], label='Close Price')
        plt.plot(data.index, data['MARS'], label='MARS', linestyle='--')
        plt.title(f"{symbol} Price and MARS")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.legend()
        plot_path = os.path.join(PLOTS_DIR, f"{symbol}_mars.png")
        plt.savefig(plot_path)
        plt.close()
        return plot_path
    except Exception as e:
        logger.error(f"Error generating plot for {symbol}: {e}")
        return None

def send_telegram_message(message, image_path=None):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        response = requests.post(url, data=data)
        if image_path:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
            with open(image_path, 'rb') as photo:
                files = {'photo': photo}
                data = {"chat_id": TELEGRAM_CHAT_ID}
                response = requests.post(url, files=files, data=data)
        if response.status_code != 200:
            logger.error(f"Telegram API error: {response.text}")
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {e}")

def main():
    symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
    for symbol in symbols:
        data = fetch_stock_data(symbol)
        if data is None:
            continue
        data = calculate_mars(data)
        if data is None or 'MARS' not in data.columns:
            continue
        # Example signal condition: MARS crosses above Close price
        if data['MARS'].iloc[-1] > data['Close'].iloc[-1]:
            message = f"📈 Buy Signal for {symbol} on {datetime.now().strftime('%Y-%m-%d')}"
            plot_path = generate_plot(data, symbol)
            send_telegram_message(message, plot_path)
        else:
            logger.info(f"No signal for {symbol}")

if __name__ == "__main__":
    main()
