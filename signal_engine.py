import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import requests

def fetch_price_history(symbol, interval="1m", limit=100):
    url = f"https://api.pro.coinbase.com/products/{symbol}-USDT/candles?granularity=60&limit={limit}"
    try:
        response = requests.get(url)
        data = response.json()
        prices = sorted(data, key=lambda x: x[0])  # sort by time
        return [row[4] for row in prices]  # close prices
    except:
        return []

def generate_signals():
    coins = ["BTC", "ETH", "PEPE", "AVAX", "LTC", "MATIC", "ARB", "RNDR", "OP", "ADA",
             "INJ", "SUI", "DOGE", "XRP", "BLUR", "DYDX", "APT", "SOL", "DOT", "IMX"]

    rows = []
    for coin in coins:
        history = fetch_price_history(coin)
        if len(history) < 20:
            continue

        prices = pd.Series(history)
        rsi = RSIIndicator(close=prices).rsi().iloc[-1]
        ema9 = EMAIndicator(close=prices, window=9).ema_indicator().iloc[-1]
        ema21 = EMAIndicator(close=prices, window=21).ema_indicator().iloc[-1]
        price_now = prices.iloc[-1]
        support = min(prices[-10:])
        resistance = max(prices[-10:])
        score = 0
        signal = "WAIT"

        if price_now > ema9 > ema21 and rsi > 60:
            signal = "STRONG BUY"
            score = 90
        elif price_now > ema9 and rsi > 50:
            signal = "BUY"
            score = 75
        elif price_now < ema21 and rsi < 40:
            signal = "SELL"
            score = 30

        row = {
            "Symbol": coin,
            "Price History": prices.tolist(),
            "RSI": round(rsi, 2),
            "EMA9": round(ema9, 4),
            "EMA21": round(ema21, 4),
            "Support": round(support, 4),
            "Resistance": round(resistance, 4),
            "Buy Price": round(price_now, 4),
            "SL": round(support * 0.98, 4),
            "TP": round(resistance * 0.96, 4),
            "Signal": signal,
            "Score": score
        }

        rows.append(row)

    return pd.DataFrame(rows)