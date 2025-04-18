import pandas as pd

def calculate_mars(data):
    try:
        # Sample MARS logic: simplified momentum
        data["MARS"] = data["Close"].pct_change(periods=3).rolling(window=3).mean() * 100
        return data
    except Exception as e:
        print(f"Error in MARS calculation: {e}")
        return data
