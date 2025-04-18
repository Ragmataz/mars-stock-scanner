import matplotlib.pyplot as plt

def plot_mars_chart(dates, mars_values, signals, title="MARS Chart"):
    plt.figure(figsize=(12, 6))
    plt.plot(dates, mars_values, label="MARS", color="blue")
    plt.axhline(0, color='gray', linestyle='--')

    for i, signal in enumerate(signals):
        if signal == "BUY":
            plt.text(dates[i], mars_values[i], "✅", fontsize=12, ha='center')
        elif signal == "SELL":
            plt.text(dates[i], mars_values[i], "🚨", fontsize=12, ha='center')

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("MARS Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
