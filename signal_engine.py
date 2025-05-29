import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import random
from websocket_client import get_latest_price

# List of tracked symbols (can be updated dynamically)
SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "LTC-USD",
    "OP-USD", "INJ-USD", "PEPE-USD", "DOGE-USD", "ADA-USD",
    "MATIC-USD", "BCH-USD", "DOT-USD", "RNDR-USD", "AR-USD",
    "TON-USD", "WCFG-USD", "WLD-USD", "SUI-USD", "BONK-USD"
]

def generate_signals():
    rows = []
    for symbol in SYMBOLS:
        price = get_latest_price(symbol)
        if price is None:
            continue

        df = simulate_price_data(symbol, price)
        if df is None or df.empty:
            continue

        df['EMA9'] = EMAIndicator(df['close'], window=9).ema_indicator()
        df['EMA21'] = EMAIndicator(df['close'], window=21).ema_indicator()
        df['RSI'] = RSIIndicator(df['close'], window=14).rsi()

        latest = df.iloc[-1]
        signal = detect_signal(latest)
        score = compute_score(latest)
        support, resistance = get_support_resistance(df)
        strategy, advice = determine_strategy_and_advice(latest, signal, support)

        if signal != "WAIT":
            rows.append({
                "Symbol": symbol,
                "Current Price": round(price, 8),
                "RSI": round(latest['RSI'], 2),
                "Signal": signal,
                "Score": score,
                "Support": support,
                "Resistance": resistance,
                "Buy Price": round(price, 8),
                "Take Profit": round(price * 1.01, 8),
                "Stop Loss": round(price * 0.99, 8),
                "Strategy": strategy,
                "Advice": advice
            })

    df_result = pd.DataFrame(rows)
    return df_result.sort_values(by="Score", ascending=False).reset_index(drop=True)

def simulate_price_data(symbol, price):
    # Simulate 50 candles with small variations
    prices = [price + random.uniform(-0.5, 0.5) for _ in range(50)]
    df = pd.DataFrame(prices, columns=["close"])
    return df

def detect_signal(latest):
    if latest['RSI'] < 30 and latest['EMA9'] > latest['EMA21']:
        return "BUY"
    elif latest['RSI'] > 70 and latest['EMA9'] < latest['EMA21']:
        return "SELL"
    else:
        return "WAIT"

def compute_score(latest):
    score = 0
    if latest['EMA9'] > latest['EMA21']:
        score += 1
    if latest['RSI'] < 30:
        score += 1
    elif latest['RSI'] > 70:
        score -= 1
    return score

def get_support_resistance(df):
    support = round(min(df['close'][-10:]), 8)
    resistance = round(max(df['close'][-10:]), 8)
    return support, resistance

def determine_strategy_and_advice(latest, signal, support):
    if signal == "BUY":
        strategy = "Scalping"
        advice = "Entry near support. Set SL & TP carefully."
    elif signal == "SELL":
        strategy = "Short"
        advice = "Market looks overbought. Short with caution."
    else:
        strategy = "Wait"
        advice = "No clear setup. Wait for better opportunity."
    return strategy, advice