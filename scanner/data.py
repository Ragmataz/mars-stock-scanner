import yfinance as yf
import pandas as pd
import logging

log = logging.getLogger()

def get_data(symbol: str, interval: str) -> pd.DataFrame | None:
    interval_map = {
        "Daily": ("6mo", "1d"),
        "Weekly": ("1y", "1wk"),
        "Monthly": ("2y", "1mo")
    }

    if interval not in interval_map:
        log.error(f"Unknown interval: {interval}")
        return None

    period, yf_interval = interval_map[interval]

    try:
        df = yf.download(
            symbol,
            period=period,
            interval=yf_interval,
            progress=False,
            auto_adjust=False,
            threads=False,
        )

        if df.empty or "Close" not in df.columns:
            log.error(f"No data returned for {symbol} [{interval}]")
            return None

        df.dropna(inplace=True)
        return df

    except Exception as e:
        log.error(f"Exception fetching data for {symbol} [{interval}]: {e}")
        return None
