def plot_stock_chart(df, symbol, timeframe="Daily"):
    import matplotlib.pyplot as plt
    import os

    try:
        plt.figure(figsize=(10, 5))
        plt.plot(df['Close'], label='Close Price', linewidth=2)
        plt.plot(df['MARS'], label='MARS', linestyle='--')
        plt.title(f"{symbol} - {timeframe}")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.legend()
        filename = f"{symbol.replace('.NS','')}_{timeframe}.png"
        filepath = os.path.join("/tmp", filename)
        plt.savefig(filepath)
        plt.close()
        return filepath
    except Exception as e:
        print(f"Error plotting chart: {e}")
        return None
