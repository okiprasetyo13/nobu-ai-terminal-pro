# signal_engine.py (Production - Yanto Bubut Logic)
def generate_all_signals(coin_list, price_fetcher):
    import pandas as pd
    rows = []
    for symbol in coin_list:
        price = price_fetcher(symbol)
        if price is None:
            continue  # Skip broken data

        support = price * 0.97
        resistance = price * 1.03
        sl = support * 0.995
        tp = resistance * 0.997

        rsi = 40  # Placeholder (you can replace with real RSI calc)
        ema_cross = True
        vol_spike = True
        near_support = price <= support * 1.003

        buy = sl_val = tp_val = None
        advice = "Wait for conditions"

        if rsi > 35 and ema_cross and vol_spike and near_support:
            buy = price
            sl_val = sl
            tp_val = tp
            advice = f"Buy at {price:.8f}, TP at {tp:.8f}, SL at {sl:.8f} (Yanto scalp setup)"

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
            "Score": 90 if buy else 50,
            "Expert Advice": advice
        })

    df = pd.DataFrame(rows)
    return df.sort_values(by="Score", ascending=False).head(10)
