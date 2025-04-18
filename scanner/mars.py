def calculate_mars(data):
    try:
        data['EMA5'] = data['Close'].ewm(span=5, adjust=False).mean()
        data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
        data['MARS'] = data['EMA5'] - data['EMA20']

        signal = None
        if data['MARS'].iloc[-2] < 0 and data['MARS'].iloc[-1] > 0:
            signal = 'BUY'
        elif data['MARS'].iloc[-2] > 0 and data['MARS'].iloc[-1] < 0:
            signal = 'SELL'

        return signal, data
    except Exception as e:
        print("Error in MARS calculation:", e)
        return None, data
