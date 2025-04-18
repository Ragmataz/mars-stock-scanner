import matplotlib.pyplot as plt

def plot_mars_chart(data, symbol, timeframe):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data['Close'], label='Close Price', color='blue')
    plt.plot(data.index, data['EMA5'], label='EMA 5', color='green')
    plt.plot(data.index, data['EMA20'], label='EMA 20', color='red')
    plt.title(f"MARS Chart: {symbol} ({timeframe})")
    plt.legend()
    filepath = f"/tmp/{symbol.replace('.', '_')}_{timeframe}.png"
    plt.savefig(filepath)
    plt.close()
    return filepath
