import requests
import random
import pandas as pd   # ✅ Keep this here globally
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator, MACD
from websocket_client import get_latest_price, get_ohlcv_data

def get_top_coinbase_symbols():
    try:
        url = "https://api.exchange.coinbase.com/products"
        res = requests.get(url).json()
        usd_pairs = [p for p in res if p.get("quote_currency") == "USD" and p.get("status") == "online"]
        sorted_pairs = sorted(usd_pairs, key=lambda x: float(x.get("volume_24h", 0)), reverse=True)

        symbols = []
        for item in sorted_pairs:
            base = item.get("base_currency")
            if base not in symbols:
                symbols.append(base)
            if len(symbols) >= 20:
                break
        return symbols
    except Exception as e:
        print(f"[❌] Failed to fetch dynamic symbols: {e}")
        return [
            'SOL', 'APT', 'AVAX', 'OP', 'ARB', 'PEPE', 'DOGE', 'LTC',
            'MATIC', 'SUI', 'INJ', 'LINK', 'RNDR', 'WIF', 'BLUR', 'SHIB', 'TIA', 'JUP'
        ]

def find_last_local_min(df):
    for i in range(len(df) - 2, 1, -1):
        if df['close'].iloc[i] < df['close'].iloc[i - 1] and df['close'].iloc[i] < df['close'].iloc[i + 1]:
            return df['close'].iloc[i]
    return df['close'].min()

def find_last_local_max(df):
    for i in range(len(df) - 2, 1, -1):
        if df['close'].iloc[i] > df['close'].iloc[i - 1] and df['close'].iloc[i] > df['close'].iloc[i + 1]:
            return df['close'].iloc[i]
    return df['close'].max()

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
    # ✅ Always prioritize BTC and ETH first
    priority_symbols = ['BTC', 'ETH']
    other_symbols = get_top_coinbase_symbols()
    other_symbols = [s for s in other_symbols if s not in priority_symbols]
    
    # 🚀 Process BTC and ETH first, allow them to bypass filters
    for symbol in priority_symbols:
        try:
            df = get_m1_ohlcv(symbol)
            if df is None or df.empty or len(df) < 21:
                print(f"[⚠️] Skipping {symbol}: no data")
                continue

            # === Indicators
            df["EMA9"] = EMAIndicator(df["close"], window=9).ema_indicator()
            df["EMA21"] = EMAIndicator(df["close"], window=21).ema_indicator()
            df["RSI"] = RSIIndicator(df["close"], window=14).rsi()
            macd = MACD(df["close"])
            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()

            latest = df.iloc[-1]
            df["volume_avg"] = df["volume"].rolling(window=10).mean()
            volume = latest["volume"]
            volume_avg = latest["volume_avg"]
            volume_status = "📈 High" if volume > volume_avg else "📉 Low"
            support = round(find_last_local_min(df), 8)
            resistance = round(find_last_local_max(df), 8)
            entry = support * 1.01
            sl = support * 0.985
            tp = resistance

            score = 0
            if latest["EMA9"] > latest["EMA21"]:
                score += 1
            if latest["RSI"] < 30:
                score += 1
            elif latest["RSI"] > 70:
                score -= 1
            if latest["MACD"] > latest["MACD_SIGNAL"]:
                score += 1
            else:
                score -= 1

            signal = "Buy" if latest["RSI"] < 35 and latest["EMA9"] > latest["EMA21"] else "Wait"
            advice = "📌 Buy on support" if signal == "Buy" else "Watch for entry"
            strategy = "Scalping"

            row = {
                "Symbol": symbol,
                "Strategy": strategy,
                "Score": score,
                "Signal": signal,
                "Buy Price": round(entry, 4),
                "Recommended Buy": round(support * 1.01, 4),
                "Take Profit": round(tp, 4),
                "Stop Loss": round(sl, 4),
                "Support": round(support, 4),
                "Resistance": round(resistance, 4),
                "Current Price": round(latest["close"], 4),
                "RSI": round(latest["RSI"], 2),
                "EMA9": round(latest["EMA9"], 2),
                "EMA21": round(latest["EMA21"], 2),
                "Volume": int(volume),
                "Volume Status": volume_status,
                "Advice": advice,
                "Price History": df["close"].tail(30).tolist(),
            }
            signal_rows.append(row)
            print(f"[✅ BTC/ETH] Signal added for {symbol}")

        except Exception as e:
            print(f"[❌ BTC/ETH Error] {symbol}: {e}")

    for symbol in other_symbols:
        try:
            df = get_m1_ohlcv(symbol)
            if df is None or df.empty or len(df) < 21:
                print(f"[❌] Skipping {symbol}: insufficient OHLCV data.")
                continue

            df["EMA9"] = EMAIndicator(df["close"], window=9).ema_indicator()
            df["EMA21"] = EMAIndicator(df["close"], window=21).ema_indicator()
            df["RSI"] = RSIIndicator(df["close"], window=14).rsi()
            macd = MACD(df["close"])
            df["MACD"] = macd.macd()
            df["MACD_SIGNAL"] = macd.macd_signal()
            # === Volatility & Breakout Filter (define latest FIRST!) ===
            latest = df.iloc[-1]
            df["volatility"] = df["close"].rolling(window=10).std()
            low_volatility = df["volatility"].iloc[-1] < 0.002 * latest["close"]
            if low_volatility:
                print(f"[⚠️ {symbol}] Rejected: low volatility")
            recent_high = df["close"].rolling(window=15).max().iloc[-1]
            no_breakout = latest["close"] < recent_high * 0.98
            if no_breakout:
                print(f"[📉 {symbol}] No breakout above recent high")
                
            support = round(find_last_local_min(df), 8)
            resistance = round(find_last_local_max(df), 8)
            print(f"[🔍 {symbol}] Support={support}, Resistance={resistance}")
            entry = support * 1.01
            sl = support * 0.985
            tp = resistance

            score = 0
            if latest["EMA9"] > latest["EMA21"]:
                score += 1
            if latest["RSI"] < 30:
                score += 1
            elif latest["RSI"] > 70:
                score -= 1
            if latest["MACD"] > latest["MACD_SIGNAL"]:
                score += 1
            else:
                score -= 1

            signal = "Buy" if latest["RSI"] < 35 and latest["EMA9"] > latest["EMA21"] else "Wait"
            advice = "📌 Buy on support" if signal == "Buy" else "Watch for entry"
            strategy = "Scalping"

            row = {
                "Symbol": symbol,
                "Strategy": strategy,
                "Score": score,
                "Signal": signal,
                "Buy Price": round(entry, 4),
                "Recommended Buy": round(support * 1.01, 4),
                "Take Profit": round(tp, 4),
                "Stop Loss": round(sl, 4),
                "Support": round(support, 4),
                "Resistance": round(resistance, 4),
                "Current Price": round(latest["close"], 4),
                "RSI": round(latest["RSI"], 2),
                "EMA9": round(latest["EMA9"], 2),
                "EMA21": round(latest["EMA21"], 2),
                "Advice": advice,
                "Price History": df["close"].tail(30).tolist(),
            }
            signal_rows.append(row)
            print(f"[✅] Signal added for {symbol}")

        except Exception as e:
            print(f"[❌] Error processing {symbol}: {e}")

    df = pd.DataFrame(signal_rows)
    # ✅ Step 1: Exit early if no signals passed
    if df.empty:
        print("[⚠️] No valid signals generated.")
        return df
    # ✅ Step 2: Sort by Score
    df = df.sort_values(by="Score", ascending=False)
    
    # ✅ Step 3: Always include BTC & ETH, even if low score
    btc_row = df[df["Symbol"] == "BTC"]
    eth_row = df[df["Symbol"] == "ETH"]
    df_filtered = df[~df["Symbol"].isin(["BTC", "ETH"])]
    
    # ✅ Step 4: Keep only top 18 other coins to limit total to 20
    df_filtered = df_filtered.head(18)
    
    # ✅ Step 5: Combine BTC + ETH + others (always on top)
    df_final = pd.concat([btc_row, eth_row, df_filtered], ignore_index=True)
    
    print(f"[✅] Final DataFrame contains {len(df_final)} coins.")
    return df_final