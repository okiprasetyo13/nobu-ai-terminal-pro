import requests
import random
import pandas as pd   # ✅ Keep this here globally
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from websocket_client import get_latest_price, get_ohlcv_data

def get_m1_ohlcv(symbol):
    url = f"https://nobu-fastapi-price.onrender.com/ohlcv/{symbol}"
    try:
        res = requests.get(url).json()
        df = pd.DataFrame(res)
        df["time"] = pd.to_datetime(df["time"], unit="s")
        df.set_index("time", inplace=True)
        df.sort_index(inplace=True)
        return df
    except Exception as e:
        print(f"[{symbol}] OHLCV fetch failed: {e}")
        return pd.DataFrame()

def analyze_symbol(symbol):
    try:
        symbol_id = symbol.replace("-USD", "")
        df = get_m1_ohlcv(symbol_id)

        # === Indicators ===
        df['EMA9'] = EMAIndicator(close=df['close'], window=9).ema_indicator()
        df['EMA21'] = EMAIndicator(close=df['close'], window=21).ema_indicator()
        df['RSI'] = RSIIndicator(close=df['close'], window=14).rsi()
        macd = MACD(close=df['close'])
        df['MACD'] = macd.macd()
        df['MACD_SIGNAL'] = macd.macd_signal()
        df['volume_avg'] = df['volume'].rolling(window=10).mean()
        df['volatility'] = df['close'].rolling(window=10).std()

        # === Support & Resistance Detection ===
        df['local_min'] = df['close'][(df['close'].shift(1) > df['close']) & (df['close'].shift(-1) > df['close'])]
        df['local_max'] = df['close'][(df['close'].shift(1) < df['close']) & (df['close'].shift(-1) < df['close'])]
        support = df['local_min'].dropna().iloc[-1] if not df['local_min'].dropna().empty else df['close'].min()
        resistance = df['local_max'].dropna().iloc[-1] if not df['local_max'].dropna().empty else df['close'].max()

        # === Signal Decision Logic ===
        latest = df.iloc[-1]
        price = latest['close']
        rsi = latest['RSI']
        volume = latest['volume']
        volume_avg = latest['volume_avg']
        macd_value = latest['MACD']
        macd_signal = latest['MACD_SIGNAL']
        trend_strength = latest['EMA9'] - latest['EMA21']
        volatility = latest['volatility']

        if rsi < 30 and trend_strength > 0 and macd_value > macd_signal and volume > volume_avg:
            signal = "BUY"
        elif rsi > 70 and macd_value < macd_signal:
            signal = "SELL"
        else:
            signal = "WAIT"

        # === Strategy & Advice ===
        if signal == "BUY":
            advice = "Strong buy signal. RSI oversold with trend & volume confirmation."
            strategy = "Scalping"
        elif signal == "SELL":
            advice = "Overbought. Exit or consider short."
            strategy = "Short"
        else:
            advice = "No trade. Wait for confirmation."
            strategy = "Wait"

        # === Risk & Reward Calculation ===
        entry = price
        tp = resistance
        sl = support if support < entry else entry - 2 * volatility

        return {
            "Symbol": symbol.replace("-USD", ""),
            "Price": round(price, 4),
            "RSI": round(rsi, 2),
            "EMA9": round(latest['EMA9'], 2),
            "EMA21": round(latest['EMA21'], 2),
            "Support": round(support, 4),
            "Resistance": round(resistance, 4),
            "Entry": round(entry, 4),
            "SL": round(sl, 4),
            "TP": round(tp, 4),
            "Signal": signal,
            "Score": compute_score(latest),
            "Suitability": strategy,
            "Expert Tip": advice,
            "Volume": int(volume),
            "Volume Avg": int(volume_avg),
            "Price History": df['close'].tolist()
        }

    except Exception as e:
        print(f"[❌ {symbol}] Error during analysis: {e}")
        return None

def get_live_price(symbol):
    url = f"https://nobu-fastapi-price.onrender.com/price/{symbol}"
    try:
        res = requests.get(url, timeout=3)
        return float(res.json()["price"])
    except Exception as e:
        print(f"[❌] {symbol} live price error: {e}")
        return None

def generate_all_signals():
    signal_rows = []

    symbol_list = [
        'BTC', 'ETH', 'SOL', 'APT', 'AVAX', 'OP', 'ARB', 'PEPE', 'DOGE', 'LTC',
        'MATIC', 'SUI', 'INJ', 'LINK', 'RNDR', 'WIF', 'BLUR', 'SHIB', 'TIA', 'JUP'
    ]

    for symbol in symbol_list:
        try:
            base_price = get_live_price(symbol)
            if base_price is None:
                continue

            print(f"[🔄] {symbol} live price = {base_price}")
            price_history = [base_price + random.randint(-200, 200) for _ in range(10)]

            row = {
                'Symbol': symbol,
                'Strategy': 'Scalping',
                'Score': random.randint(3, 5),
                'Buy Price': base_price,
                'Take Profit': base_price + 500,
                'Stop Loss': base_price - 500,
                'Support': base_price - 300,
                'Resistance': base_price + 700,
                'Current Price': base_price,
                'Signal': 'Buy',
                'RSI': round(random.uniform(25, 40), 2),
                'EMA9': base_price - 50,
                'EMA21': base_price - 100,
                'Volume': random.randint(1000000, 50000000),
                'Advice': 'Buy on support',
                'Trade Type': 'Scalping',
                'Price History': price_history,
            }

            signal_rows.append(row)
            print(f"[✅] Signal added for {symbol}")

        except Exception as e:
            print(f"[❌] Error processing {symbol}: {e}")

    df = pd.DataFrame(signal_rows)
    print(f"[📊] Total signals generated: {len(df)}")
    return df