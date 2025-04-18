import logging
import yfinance as yf
from datetime import datetime, timedelta
from scanner.mars import calculate_mars
from scanner.plot import plot_stock_chart
from scanner.telegram_bot import send_telegram_message_with_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SYMBOLS = [
    "ADANIENT.NS", "ADANIPORTS.NS", "APOLLOHOSP.NS", "ASIANPAINT.NS", "AXISBANK.NS",
    "BAJAJ-AUTO.NS", "BAJFINANCE.NS", "BAJAJFINSV.NS", "BHARTIARTL.NS", "BPCL.NS",
    "BRITANNIA.NS", "CIPLA.NS", "COALINDIA.NS", "DIVISLAB.NS", "DRREDDY.NS",
    "EICHERMOT.NS", "GRASIM.NS", "HCLTECH.NS", "HDFC.NS", "HDFCBANK.NS",
    "HEROMOTOCO.NS", "HINDALCO.NS", "HINDUNILVR.NS", "ICICIBANK.NS", "INDUSINDBK.NS",
    "INFY.NS", "ITC.NS", "JSWSTEEL.NS", "KOTAKBANK.NS", "LT.NS",
    "M&M.NS", "MARUTI.NS", "NESTLEIND.NS", "NTPC.NS", "ONGC.NS",
    "POWERGRID.NS", "RELIANCE.NS", "SBILIFE.NS", "SBIN.NS", "SHREECEM.NS",
    "SUNPHARMA.NS", "TATACONSUM.NS", "TATAMOTORS.NS", "TATASTEEL.NS", "TCS.NS",
    "TECHM.NS", "TITAN.NS", "ULTRACEMCO.NS", "UPL.NS", "WIPRO.NS"
]


TIMEFRAMES = {
    "Daily": {"interval": "1d", "period": "6mo"},
    "Weekly": {"interval": "1wk", "period": "2y"},
    "Monthly": {"interval": "1mo", "period": "5y"},
}


def analyze_symbol(symbol, tf_name, interval, period):
    try:
        logger.info(f"Processing {symbol} [{tf_name}]")
        df = yf.download(symbol, interval=interval, period=period, auto_adjust=True)

        if df is None or df.empty:
            raise ValueError("Downloaded data is empty or None")

        df = calculate_mars(df)

        if df is None or df.empty:
            raise ValueError("Failed to calculate MARS")

        signal_msg = ""
        if df['MARS'].iloc[-1] > 0 and df['MARS'].iloc[-2] <= 0:
            signal_msg = f"✅ BUY Signal for {symbol} on {tf_name} [MARS crossover up 📈]"
        elif df['MARS'].iloc[-1] < 0 and df['MARS'].iloc[-2] >= 0:
            signal_msg = f"🚨 SELL Signal for {symbol} on {tf_name} [MARS crossover down 📉]"

        if signal_msg:
            chart_path = plot_stock_chart(df, symbol, tf_name)
            send_telegram_message_with_image(signal_msg, chart_path)
            return True

    except Exception as e:
        logger.error(f"Error processing {symbol} [{tf_name}]: {e}")

    return False


def run():
    signals_found = False
    for symbol in SYMBOLS:  # Corrected variable name from 'symbols' to 'SYMBOLS'
        for label, interval in TIMEFRAMES.items():  # Corrected variable name from 'timeframes' to 'TIMEFRAMES'
            logger.info(f"Processing {symbol} [{label}]")
            try:
                data = get_data(symbol, label, interval)  # Fix `index_symbol` to `label`
                if data is None or data.empty or 'Close' not in data.columns:
                    logger.error(f"Error processing {symbol} [{label}]: No valid data")
                    continue

                data = calculate_mars(data)
                if data['MARS'].iloc[-1] > data['Close'].iloc[-1]:
                    # generate chart and send image
                    image_path = f"{symbol}_{label}.png"
                    plot_mars_chart(data, symbol, label, image_path)
                    signal = f"📉 SELL signal for {symbol} on {label}"
                    send_telegram_message_with_image(signal, image_path)
                    signals_found = True
                elif data['MARS'].iloc[-1] < data['Close'].iloc[-1]:
                    image_path = f"{symbol}_{label}.png"
                    plot_mars_chart(data, symbol, label, image_path)
                    signal = f"✅ BUY signal for {symbol} on {label}"
                    send_telegram_message_with_image(signal, image_path)
                    signals_found = True
            except Exception as e:
                logger.error(f"Error processing {symbol} [{label}]: {e}")

    if not signals_found:
        send_telegram_message("🍼 No MARS signals on any timeframe today. Baby can nap. 😴")


if __name__ == "__main__":
    run()
