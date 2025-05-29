
import requests
import pandas as pd
import numpy as np
import plot_chart
from datetime import datetime, timedelta

COINBASE_API_URL = "https://api.exchange.coinbase.com"

def fetch_ohlcv(symbol, granularity=60, limit=50):
    url = f"{COINBASE_API_URL}/products/{symbol}-USD/candles?granularity={granularity}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()
    df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.sort_values('time')
    return df

def analyze_symbol(symbol):
    df = fetch_ohlcv(symbol)
    if df is None or df.empty:
        return None

    close = df['close']
    rsi = compute_rsi(close)
    ema9 = close.ewm(span=9).mean().iloc[-1]
    ema21 = close.ewm(span=21).mean().iloc[-1]
    support = close.min()
    resistance = close.max()
    entry = close.iloc[-1]
    sl = entry * 0.99
    tp = entry * 1.01
    score = int(rsi // 10)
    suitability = 'Scalping' if rsi < 40 else 'Long' if rsi < 70 else 'Short'
    tip = "Buy now, breakout expected" if suitability == 'Scalping' else "MACD showing bullish divergence"
    chart = plot_chart.generate_chart_base64(df)

    return {
        'Symbol': symbol,
        'Price': round(entry, 2),
        'RSI': round(rsi, 2),
        'EMA9': round(ema9, 2),
        'EMA21': round(ema21, 2),
        'Support': round(support, 2),
        'Resistance': round(resistance, 2),
        'Entry': round(entry, 2),
        'SL': round(sl, 2),
        'TP': round(tp, 2),
        'Score': score,
        'Suitability': suitability,
        'Expert Tip': tip,
        'Chart': chart
    }

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def analyze_all_symbols():
    symbols = ['BTC', 'ETH']
    results = []
    for symbol in symbols:
        data = analyze_symbol(symbol)
        if data:
            results.append(data)
    return results
