import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import random
from websocket_client import get_latest_price
from ta.trend import MACD

# Inside generate_signals():
df['MACD'] = MACD(df['close']).macd()
df['MACD_SIGNAL'] = MACD(df['close']).macd_signal()

# List of tracked symbols (can be updated dynamically)
SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "LTC-USD",
    "OP-USD", "INJ-USD", "PEPE-USD", "DOGE-USD", "ADA-USD",
    "MATIC-USD", "BCH-USD", "DOT-USD", "RNDR-USD", "AR-USD",
    "TON-USD", "WCFG-USD", "WLD-USD", "SUI-USD", "BONK-USD"
]

def generate_signals(df, symbol):
    try:
        # Calculate indicators
        df['EMA9'] = EMAIndicator(close=df['close'], window=9).ema_indicator()
        df['EMA21'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
        df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()

        # Volume-based filter
        if 'volume' in df.columns:
            df['volume_avg'] = df['volume'].rolling(window=10).mean()
            if df['volume'].iloc[-1] < df['volume_avg'].iloc[-1]:
                return None  # Skip weak volume coin

        # Trend filter: skip if not in uptrend
        if df['EMA9'].iloc[-1] < df['EMA21'].iloc[-1]:
            return None

        # Signal logic
        latest_close = df['close'].iloc[-1]
        ema9 = df['EMA9'].iloc[-1]
        ema21 = df['EMA21'].iloc[-1]
        rsi = df['RSI'].iloc[-1]

        signal = "WAIT"
        score = 0
        advice = "Stay out for now"
        trade_type = "Scalping"

        if rsi < 30 and latest_close < ema9 and latest_close < ema21:
            signal = "BUY"
            score += 2
            advice = "Potential bounce soon, consider watching"
        if ema9 > ema21 and latest_close > ema9:
            signal = "BUY"
            score += 3
            advice = "Strong upward momentum"
        if rsi > 70:
            signal = "SELL"
            score = 1
            advice = "Overbought zone, prepare to take profit"

        # Determine trade suitability
        if rsi < 35 and ema9 > ema21:
            trade_type = "Scalping"
        elif ema9 > ema21 and rsi > 50:
            trade_type = "Long Trading"
        elif ema9 < ema21 and rsi < 50:
            trade_type = "Short Trading"

        return {
            'Symbol': symbol,
            'Price': latest_close,
            'RSI': round(rsi, 2),
            'EMA9': round(ema9, 2),
            'EMA21': round(ema21, 2),
            'Signal': signal,
            'Score': score,
            'Advice': advice,
            'Trade Type': trade_type,
            'Volume': round(df['volume'].iloc[-1], 2) if 'volume' in df.columns else None,
            'Volume Avg': round(df['volume_avg'].iloc[-1], 2) if 'volume' in df.columns else None,
        }
    except Exception as e:
        print(f"[generate_signals error] {symbol}: {e}")
        return None

    df_result = pd.DataFrame(rows)

# === Dynamic Filtering and Ranking Logic ===
# 1. Filter coins in UP trend
df_filtered = df_result[(df_result['EMA9'] > df_result['EMA21']) & (df_result['Signal'] != 'WAIT')]

# 2. Filter top 20 by volume
df_filtered = df_filtered.sort_values(by="Volume", ascending=False).head(20)

# 3. Always include BTC and ETH at top
btc_row = df_result[df_result['Symbol'] == 'BTC']
eth_row = df_result[df_result['Symbol'] == 'ETH']
df_filtered = pd.concat([btc_row, eth_row, df_filtered]).drop_duplicates(subset='Symbol')

# 4. Final sorting by Score
df_ranked = df_filtered.sort_values(by="Score", ascending=False).reset_index(drop=True)

return df_ranked

def load_real_price_data(symbol):
    # Placeholder – replace with your actual loader
    df = your_get_ohlcv_function(symbol, timeframe="1m", limit=50)
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
    if latest['MACD'] > latest['MACD_SIGNAL']:
        score += 1
    else:
        score -= 1
    return score

def get_support_resistance(df):
    support = round(min(df['close'][-10:]), 8)
    resistance = round(max(df['close'][-10:]), 8)
    return support, resistance

def determine_strategy_and_advice(latest, signal, support):
    if signal == "BUY":
        if latest['RSI'] < 30:
            advice = "Oversold bounce expected. Enter near support. SL tight."
        else:
            advice = "Uptrend detected. Buy momentum continuation."
        strategy = "Scalping" if latest['EMA9'] > latest['EMA21'] else "Long"
    elif signal == "SELL":
        advice = "Overbought condition. Consider shorting or exiting."
        strategy = "Short"
    else:
        advice = "No setup now. Monitor closely for breakout/retest."
        strategy = "Wait"
    return strategy, advice