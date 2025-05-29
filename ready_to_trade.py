def is_ready_to_trade(signal, rsi, signal_score, trade_suitability):
    """
    Determines if a coin is ready to trade.

    :param signal: Buy/Sell/Hold
    :param rsi: Relative Strength Index (float)
    :param signal_score: Score indicating signal strength (float)
    :param trade_suitability: One of ['Scalping', 'Long', 'Short']
    :return: Boolean (True = ready to trade)
    """
    if signal == "Buy" and rsi < 35 and signal_score >= 7 and trade_suitability in ["Scalping", "Long"]:
        return True
    elif signal == "Sell" and rsi > 70 and signal_score >= 7 and trade_suitability == "Short":
        return True
    return False


def get_expert_advice(signal, buy_price, sl, tp, suitability):
    """
    Returns a formatted expert advice string.

    :param signal: Buy/Sell/Hold
    :param buy_price: Suggested entry price
    :param sl: Stop Loss price
    :param tp: Take Profit price
    :param suitability: Scalping/Long/Short
    :return: String with actionable insights
    """
    if signal == "Buy":
        return f"✅ <b>Entry:</b> {buy_price}\n🎯 <b>TP:</b> {tp}\n🛑 <b>SL:</b> {sl}\n🧠 Strategy: {suitability}"
    elif signal == "Sell":
        return f"⚠️ <b>Sell Signal</b>\n🎯 <b>TP:</b> {tp}\n🛑 <b>SL:</b> {sl}\n🧠 Strategy: {suitability}"
    else:
        return f"⏸️ <b>Hold</b>\n🧠 Strategy: {suitability}\n📊 Monitor for better setup"