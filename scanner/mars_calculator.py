import pandas as pd

def calculate_mars(df: pd.DataFrame) -> pd.Series:
    """
    Calculates MARS = (Stock % change - Index % change) over the last 14 periods.
    """
    stock_returns = df['Close'].pct_change(14) * 100
    index_returns = df['Index_Close'].pct_change(14) * 100
    mars = stock_returns - index_returns
    return mars
