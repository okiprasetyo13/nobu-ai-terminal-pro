def expert_trade_suggestion(price, support, resistance, signal):
    if price is None or support is None or resistance is None:
        return "⛔️ Insufficient data"
    
    try:
        price = float(price)
        support = float(support)
        resistance = float(resistance)
    except:
        return "⚠️ Invalid values"

    buffer = 0.002  # tolerance for buy zone
    trade_type = ""

    if signal == "STRONG BUY" or (price <= support * (1 + buffer)):
        trade_type = "SCALPING BUY"
        tp = round((price + (resistance - price) * 0.6), 4)
        return f"💰 Buy Now\n🎯 TP: {tp}\n🛑 SL: {support * 0.98:.4f}\n🔁 Type: {trade_type}"
    elif price >= resistance:
        return "⚠️ Overbought - Wait"
    elif signal == "SELL":
        return "🔻 Consider SHORT"
    else:
        return "🤔 Wait for signal"