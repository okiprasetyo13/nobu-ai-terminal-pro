import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from websocket_client import get_latest_price
from websocket_client import get_ohlcv_data

SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "LTC-USD",
    "OP-USD", "INJ-USD", "PEPE-USD", "DOGE-USD", "ADA-USD",
    "MATIC-USD", "BCH-USD", "DOT-USD", "RNDR-USD", "AR-USD",
    "TON-USD", "WCFG-USD", "WLD-USD", "SUI-USD", "BONK-USD"
]

def analyze_symbol(symbol):
    try:
        df = your_get_ohlcv_function(symbol, timeframe="1m", limit=50)
        df['EMA9'] = EMAIndicator(close=df['close'], window=9).ema_indicator()
        df['EMA21'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
        df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()
        df['MACD'] = MACD(df['close']).macd()
        df['MACD_SIGNAL'] = MACD(df['close']).macd_signal()

        if 'volume' in df.columns:
            df['volume_avg'] = df['volume'].rolling(window=10).mean()
            if df['volume'].iloc[-1] < df['volume_avg'].iloc[-1]:
                return None

        if df['EMA9'].iloc[-1] < df['EMA21'].iloc[-1]:
            return None

        latest = df.iloc[-1]
        price = latest['close']
        rsi = latest['RSI']
        ema9 = latest['EMA9']
        ema21 = latest['EMA21']
        macd = latest['MACD']
        macd_signal = latest['MACD_SIGNAL']
        volume = latest['volume'] if 'volume' in latest else None
        volume_avg = df['volume_avg'].iloc[-1] if 'volume_avg' in df else None
        support, resistance = get_support_resistance(df)
        signal = detect_signal(latest)
        score = compute_score(latest)
        strategy, advice = determine_strategy_and_advice(latest, signal, support)
        entry = support * 1.01
        tp = resistance
        sl = support * 0.985

        return {
            "Symbol": symbol.replace("-USD", ""),
            "Price": round(price, 2),
            "RSI": round(rsi, 2),
            "EMA9": round(ema9, 2),
            "EMA21": round(ema21, 2),
            "Support": round(support, 2),
            "Resistance": round(resistance, 2),
            "Entry": round(entry, 2),
            "SL": round(sl, 2),
            "TP": round(tp, 2),
            "Signal": signal,
            "Score": score,
            "Suitability": strategy,
            "Expert Tip": advice,
            "Volume": round(volume, 2) if volume else None,
            "Volume Avg": round(volume_avg, 2) if volume_avg else None,
            "Price History": df['close'].tolist()
        }

    except Exception as e:
        print(f"[{symbol}] Error: {e}")
        return None

def generate_signals(df, symbol):
    rows = []
    for symbol in SYMBOLS:
        data = analyze_symbol(symbol)
        if data:
            rows.append(data)

    if not rows:
        return pd.DataFrame()

    df_result = pd.DataFrame(rows)

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

# Helper functions
def load_real_price_data(symbol):
    from websocket_client import get_ohlcv_data
    return get_ohlcv_data(symbol)

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

symbol_list = [
    'BTC', 'ETH', 'SOL', 'APT', 'AVAX', 'OP', 'ARB', 'PEPE', 'DOGE', 'LTC',
    'MATIC', 'SUI', 'INJ', 'LINK', 'RNDR', 'WIF', 'BLUR', 'SHIB', 'TIA', 'JUP'
]

def generate_all_signals():
    import pandas as pd

    signal_rows = []

    # TEMP: Manually use 20 scalping coins
    symbol_list = [
        'BTC', 'ETH', 'SOL', 'APT', 'AVAX', 'OP', 'ARB', 'PEPE', 'DOGE', 'LTC',
        'MATIC', 'SUI', 'INJ', 'LINK', 'RNDR', 'WIF', 'BLUR', 'SHIB', 'TIA', 'JUP'
    ]

    for symbol in symbol_list:
        print(f"[CHECKING] {symbol} - Generating signal...")

        try:
            # TODO: Replace this with real signal logic
            # Dummy signal logic for now
            score = 4
            strategy = "Scalping"

            if score >= 4:
                row = {
                    'Symbol': symbol,
                    'Strategy': strategy,
                    'Score': score,
                    'Take Profit': 108000,
                    'Stop Loss': 105000,
                    'Buy Price': 106500,
                    'Support': 105000,
                    'Resistance': 108500,
                    'Current Price': 106500,
                    'Signal': 'Buy',
                    'RSI': 35,
                    'EMA9': 106400,
                    'EMA21': 106200,
                    'Volume': 50000000,
                    'Advice': 'Buy on support',
                    'Trade Type': 'Scalping',
                    'Price History': [106000, 106200, 106400, 106500, 106300],  # added for mini chart
                }
                signal_rows.append(row)
                print(f"[RESULT] {symbol} ✅ Added to signals")
            else:
                print(f"[SKIPPED] {symbol} ❌ Score too low")

        except Exception as e:
            print(f"[ERROR] {symbol} crashed: {e}")

    # Final log
    print(f"[SUMMARY] Total signals generated: {len(signal_rows)}")

    if not signal_rows:
        print("[WARNING] No valid signals. Adding BTC dummy row.")
        signal_rows.append({
            'Symbol': 'BTC',
            'Strategy': 'Scalping',
            'Score': 5,
            'Take Profit': 108000,
            'Stop Loss': 105000,
            'Buy Price': 106500,
            'Support': 105000,
            'Resistance': 108500,
            'Current Price': 106500,
            'Signal': 'Buy',
            'RSI': 35,
            'EMA9': 106400,
            'EMA21': 106200,
            'Volume': 50000000,
            'Expert Advice': 'Buy on support',
            'Trade Type': 'Scalping',
            'Price History': [106000, 106200, 106400, 106500, 106300],  # added for mini chart
        })

    return pd.DataFrame(signal_rows)

    # === Dynamic Filtering and Ranking Logic ===
    df_filtered = df_result[(df_result['EMA9'] > df_result['EMA21']) & (df_result['Signal'] != 'WAIT')]
    df_filtered = df_filtered.sort_values(by="Volume", ascending=False).head(20)

    # Always include BTC and ETH
    btc_row = df_result[df_result['Symbol'] == 'BTC-USD']
    eth_row = df_result[df_result['Symbol'] == 'ETH-USD']
    df_filtered = pd.concat([btc_row, eth_row, df_filtered]).drop_duplicates(subset='Symbol')

    # Final sorting by Score
    df_ranked = df_filtered.sort_values(by="Score", ascending=False).reset_index(drop=True)
    return df_ranked