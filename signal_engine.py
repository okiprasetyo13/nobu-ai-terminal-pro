import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import random

# Example support/resistance levels (in practice use technical analysis or data source)
SUPPORT_LEVELS = {
    'BTC': 62000, 'ETH': 3200, 'SOL': 150, 'AVAX': 35, 'LTC': 80,
    'ADA': 0.45, 'DOGE': 0.08, 'PEPE': 0.0000012, 'SHIB': 0.000024
}

RESISTANCE_LEVELS = {
    'BTC': 67500, 'ETH': 3550, 'SOL': 165, 'AVAX': 42, 'LTC': 90,
    'ADA': 0.53, 'DOGE': 0.093, 'PEPE': 0.0000015, 'SHIB': 0.000027
}

def generate_signals(live_prices):
    rows = []
    for symbol, price in live_prices.items():
        support = SUPPORT_LEVELS.get(symbol, round(price * 0.97, 4))
        resistance = RESISTANCE_LEVELS.get(symbol, round(price * 1.03, 4))

        rsi = random.randint(20, 80)
        ema9 = round(price * 0.995, 4)
        ema21 = round(price * 1.005, 4)

        score = calculate_signal_score(price, support, resistance, rsi, ema9, ema21)
        expert_advice = generate_expert_advice(price, support, resistance, score)

        sl = round(support * 0.985, 8)
        tp = round(resistance * 0.98, 8)
        buy_price = round(support * 1.01, 8)
        volume = random.randint(500000, 50000000)

        rows.append({
            'Symbol': symbol,
            'Current Price': price,
            'Support': support,
            'Resistance': resistance,
            'Buy Price': buy_price,
            'SL': sl,
            'TP': tp,
            'RSI': rsi,
            'EMA9': ema9,
            'EMA21': ema21,
            'Signal Score': score,
            'Expert Advice': expert_advice,
            'Volume': volume
        })

    df = pd.DataFrame(rows)
    df = df.sort_values(by='Signal Score', ascending=False).head(20)
    return df


def calculate_signal_score(price, support, resistance, rsi, ema9, ema21):
    score = 0
    if price <= support * 1.02:
        score += 2
    if price >= resistance * 0.98:
        score -= 2
    if rsi < 30:
        score += 2
    elif rsi > 70:
        score -= 1
    if ema9 > ema21:
        score += 1
    return score


def generate_expert_advice(price, support, resistance, score):
    if score >= 3:
        return "✅ Scalping Buy Now. TP near resistance. SL just below support."
    elif score >= 1:
        return "⚠️ Monitor closely. Might break support for bounce. Wait for confirmation."
    elif score <= -1:
        return "⛔ Not recommended now. Wait for a new setup or news trigger."
    else:
        return "Neutral – Low volatility or no trend. Avoid trading."