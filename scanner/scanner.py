import os
import matplotlib.pyplot as plt
from datetime import datetime
from scanner.fetch_data import get_data, get_nse500_list, get_index_symbol
from scanner.mars_calculator import calculate_mars
from scanner.telegram import send_telegram_message, send_telegram_photo

def detect_signals(mars_values):
    if mars_values is None or mars_values.empty:
        return None

    latest_val = mars_values.iloc[-1]
    prev_val = mars_values.iloc[-2]

    if prev_val < 0 < latest_val or (0 <= latest_val <= 2):
        return 'buy'
    elif prev_val > 0 > latest_val or (-2 <= latest_val <= 0):
        return 'sell'
    return None

def plot_mars_chart(symbol, mars_values):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(mars_values.index, mars_values.values, label="MARS", color="blue", linewidth=2)
    ax.axhline(0, color="black", linestyle="--", linewidth=1)

    # Add emoji markers
    for i in range(1, len(mars_values)):
        prev, curr = mars_values.iloc[i-1], mars_values.iloc[i]
        if prev < 0 < curr:
            ax.text(mars_values.index[i], curr + 1, '✅', fontsize=14, ha='center')
        elif prev > 0 > curr:
            ax.text(mars_values.index[i], curr - 1, '🚨', fontsize=14, ha='center')

    ax.set_title(f"{symbol} - MARS")
    ax.set_ylabel("MARS Value")
    ax.grid(True)
    plt.tight_layout()

    chart_filename = f"{symbol.replace(':', '_')}_mars_chart.png"
    plt.savefig(chart_filename)
    plt.close()
    return chart_filename

def run():
    timeframe = "1d"
    nse500_symbols = get_nse500_list()
    index_symbol = get_index_symbol("CNX500")

    buy_signals, sell_signals = [], []

    for symbol in nse500_symbols:
        try:
            df_stock = get_data(symbol, timeframe)
            df_index = get_data(index_symbol, timeframe)

            if df_stock is None or df_index is None:
                continue

            mars_values = calculate_mars(df_stock, df_index)
            signal = detect_signals(mars_values)

            if signal == 'buy':
                buy_signals.append(symbol)
            elif signal == 'sell':
                sell_signals.append(symbol)

                # Send chart for each signal (optional)
            if signal:
                chart_path = plot_mars_chart(symbol, mars_values)
                caption = f"*{symbol}* triggered a *{signal.upper()}* signal {'✅' if signal == 'buy' else '🚨'}"
                send_telegram_photo(chart_path, caption=caption)
                os.remove(chart_path)  # Clean up

        except Exception as e:
            print(f"Error processing {symbol}: {e}")
            continue

    if buy_signals or sell_signals:
        message = "*📈 MARS Signal Report*\n"
        if buy_signals:
            message += f"\n✅ *Buy Signals*:\n" + "\n".join(buy_signals)
        if sell_signals:
            message += f"\n\n🚨 *Sell Signals*:\n" + "\n".join(sell_signals)
        send_telegram_message(message)
    else:
        send_telegram_message("No MARS signals today 😴")

if __name__ == "__main__":
    run()
