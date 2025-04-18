def calculate_mars(data_dict):
    results = []
    for symbol, df in data_dict.items():
        if len(df) < 50:
            continue
        df['SMA_10'] = df['Close'].rolling(window=10).mean()
        df['SMA_30'] = df['Close'].rolling(window=30).mean()

        if df['SMA_10'].iloc[-1] > df['SMA_30'].iloc[-1] and df['SMA_10'].iloc[-2] <= df['SMA_30'].iloc[-2]:
            results.append(f"{symbol} - MARS crossover detected")

    return results
