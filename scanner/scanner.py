# scanner/scanner.py

from scanner.fetch_data import get_data, get_nse500_list, get_index_symbol
from scanner.mars import compute_mars
from scanner.telegram import send_telegram_message

def scan_stocks(timeframes=["1d", "1wk", "1mo"], ma_type="SMA", ma_len=50):
    results = {tf: [] for tf in timeframes}
    index_symbol = get_index_symbol("CNX500")
    
    index_data = {tf: get_data(index_symbol, interval=tf) for tf in timeframes}
    stocks = get_nse500_list()

    for stock in stocks:
        try:
            for tf in timeframes:
                stock_data = get_data(f"{stock}.NS", interval=tf)
                mars = compute_mars(stock_data, index_data[tf], ma_type, ma_len)
                if mars.iloc[-1] > 0 and mars.iloc[-2] <= 0:  # crossing zero
                    results[tf].append(stock)
        except Exception as e:
            continue
    
    message = ""
    for tf, symbols in results.items():
        if symbols:
            message += f"🕒 **{tf.upper()} Zero Cross:**\n" + ", ".join(symbols) + "\n\n"
    
    if message:
        send_telegram_message(message)

