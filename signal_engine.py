import pandas as pd
import numpy as np
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from plot_chart import generate_chart_base64

# Simulate fetching historical price data (you should replace this with your real API/WebSocket data)
def get_price_history(symbol, length=50):
    np.random.seed(hash(symbol) % 10000)
    base_price = 10000 if symbol == "BTC" else 2000
    prices = base_price + np.cumsum(np.random.randn(length)) * 10
    return prices.tolist()

# Determine trade suitability
def determine_trade_type(rsi, ema9, ema21):
    if rsi < 30 and ema9 > ema21:
        return "Scalping"
    elif ema9 > ema21:
        return "Long"
    elif ema9 < ema21:
        return "Short"
    else:
        return "Neutral"

# Calculate score based on signal strength
def calculate_score(rsi, ema9, ema21):
    score = 0
    if 30 < rsi < 70:
        score += 1
    if ema9 > ema21:
        score += 2
    if abs(ema9 - ema21) / ema21 < 0.02:
        score += 1
    return min(score, 5)

# Expert tip generation
def generate_expert_tip(rsi, signal_type):
    if signal_type == "Scalping":
        return "Buy now, breakout expected"
    elif signal_type == "Long":
        return "MACD showing bullish divergence"
    elif signal_type == "Short":
        return "Caution: MACD weakening"
    else:
        return "Wait for clearer signal"

# Main function
def analyze_all_symbols():
    symbols = ["BTC", "ETH"]  # Replace with dynamic list if needed
    rows = []

    for sym in symbols:
        price_history = get_price_history(sym)
        close_series = pd.Series(price_history)

        rsi = RSIIndicator(close_series).rsi().iloc[-1]
        ema9 = EMAIndicator(close_series, window=9).ema_indicator().iloc[-1]
        ema21 = EMAIndicator(close_series, window=21).ema_indicator().iloc[-1]

        current_price = close_series.iloc[-1]
        support = close_series.min()
        resistance = close_series.max()
        entry = current_price
        sl = support * 0.98
        tp = resistance * 1.01
        score = calculate_score(rsi, ema9, ema21)
        suitability = determine_trade_type(rsi, ema9, ema21)
        expert_tip = generate_expert_tip(rsi, suitability)
        chart = generate_chart_base64(close_series)

        rows.append({
            "Symbol": sym,
            "Price": round(current_price, 2),
            "RSI": round(rsi, 2),
            "EMA9": round(ema9, 2),
            "EMA21": round(ema21, 2),
            "Support": round(support, 2),
            "Resistance": round(resistance, 2),
            "Entry": round(entry, 2),
            "SL": round(sl, 2),
            "TP": round(tp, 2),
            "Score": score,
            "Suitability": suitability,
            "Expert Tip": expert_tip,
            "Chart": chart,
            "Price History": price_history
        })

    return pd.DataFrame(rows)