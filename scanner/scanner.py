def detect_mars_signal(mars_values):
    signals = []
    for i in range(1, len(mars_values)):
        prev = mars_values[i - 1]
        curr = mars_values[i]

        # ✅ BUY signal: crossing from below 0 into the range 0 to +2
        if prev < 0 and 0 <= curr <= 2:
            signals.append("BUY")

        # 🚨 SELL signal: crossing from above 0 into the range 0 to -2
        elif prev > 0 and -2 <= curr <= 0:
            signals.append("SELL")

        else:
            signals.append("")
    signals.insert(0, "")  # No signal for the very first data point
    return signals
