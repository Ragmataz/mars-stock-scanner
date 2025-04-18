import logging
from scanner.data import get_data
from scanner.mars import calculate_mars
from scanner.telegram_bot import send_telegram_message, send_telegram_message_with_image
from scanner.chart import plot_mars_chart

logging.basicConfig(level=logging.INFO)

NIFTY50_SYMBOLS = [
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "HINDUNILVR.NS", "ITC.NS", "LT.NS", "KOTAKBANK.NS", "SBIN.NS",
    "AXISBANK.NS", "BAJFINANCE.NS", "BHARTIARTL.NS", "ASIANPAINT.NS",
    "WIPRO.NS"
]

TIMEFRAMES = {
    "Daily": "1d",
    "Weekly": "1wk",
    "Monthly": "1mo"
}

def run():
    signals_found = False
    for symbol in NIFTY50_SYMBOLS:
        for label, interval in TIMEFRAMES.items():
            logging.info(f"Processing {symbol} [{label}]")
            try:
                data = get_data(symbol, None, interval)
                if data is None:
                    raise ValueError("No data returned")
                signal, enriched = calculate_mars(data)
                if signal:
                    emoji = '✅' if signal == 'BUY' else '🚨'
                    chart_path = plot_mars_chart(enriched, symbol, label)
                    msg = f"{emoji} <b>{signal}</b> signal on <b>{symbol}</b> [{label}]"
                    send_telegram_message_with_image(msg, chart_path)
                    signals_found = True
            except Exception as e:
                logging.error(f"Error processing {symbol} [{label}]: {e}")

    if not signals_found:
        send_telegram_message("🍼 No MARS signals on any timeframe today. Baby can nap. 😴")

if __name__ == '__main__':
    run()
