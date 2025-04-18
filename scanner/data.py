import yfinance as yf
import logging

def get_data(symbol: str, timeframe: str, index_symbol: str = None):
    """
    Fetches historical data for the given symbol and timeframe using yfinance.

    Args:
        symbol (str): Stock symbol (e.g., 'RELIANCE.NS').
        timeframe (str): One of ['Daily', 'Weekly', 'Monthly'].
        index_symbol (str, optional): Not used currently, placeholder for index comparison logic.

    Returns:
        DataFrame: Historical OHLCV data or None if fetching fails.
    """
    try:
        interval_map = {
            "Daily": "1d",
            "Weekly": "1wk",
            "Monthly": "1mo"
        }

        interval = interval_map.get(timeframe)
        if not interval:
            raise ValueError(f"Unsupported timeframe: {timeframe}")

        df = yf.download(symbol, period="6mo", interval=interval, auto_adjust=True, progress=False)
        
        if df.empty:
            raise ValueError("No data returned")

        df.reset_index(inplace=True)
        df.dropna(inplace=True)

        return df

    except Exception as e:
        logging.error(f"Error fetching data for {symbol} [{timeframe}]: {e}")
        return None
