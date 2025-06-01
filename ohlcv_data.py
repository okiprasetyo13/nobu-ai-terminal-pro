# ohlcv_data.py – Public Safe OHLCV Fetch from Coinbase (no API key)
import pandas as pd
import requests

def get_ohlcv(symbol: str, granularity: int = 60) -> pd.DataFrame:
    product_id = symbol.replace('/', '-').upper()  # e.g. BTC-USD
    url = f"https://api.exchange.coinbase.com/products/{product_id}/candles?granularity={granularity}"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch OHLCV for {symbol}")
    data = response.json()
    df = pd.DataFrame(data, columns=["time", "low", "high", "open", "close", "volume"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    df = df.sort_values("time")
    return df
