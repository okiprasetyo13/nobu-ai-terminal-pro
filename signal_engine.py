# signal_engine.py – Final version using real WebSocket live price
from websocket_client import get_latest_price

def generate_all_signals(coin_list):
    import pandas as pd
    rows = []
    for symbol in coin_list:
        price = get_latest_price(symbol)
        if price is None:
            continue  # skip invalid

        support = price * 0.97
        resistance = price * 1.03
        sl = support * 0.995
        tp = resistance * 0.997

        rsi = 40  # placeholder
        ema_cross = True
        vol_spike = True
        near_support = price <= support * 1.003

        buy = sl_val = tp_val = None
        advice = "Wait for EMA cross, RSI > 35, volume spike near support"
        score = 50

        if rsi > 35 and ema_cross and vol_spike and near_support:
            buy = price
            sl_val = sl
            tp_val = tp
            advice = f"Buy at {price:.8f}, TP at {tp:.8f}, SL at {sl:.8f} (Yanto scalp setup)"
            score = 90

        rows.append({
            "Symbol": symbol,
            "Price": price,
            "RSI": rsi,
            "EMA Cross": ema_cross,
            "Volume Spike": vol_spike,
            "Support": support,
            "Resistance": resistance,
            "Buy": buy,
            "SL": sl_val,
            "TP": tp_val,
            "Score": score,
            "Expert Advice": advice
        })

    df = pd.DataFrame(rows)
    return df.sort_values(by="Score", ascending=False).head(10)
