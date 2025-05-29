import requests

# Set your Telegram credentials
TELEGRAM_BOT_TOKEN = "8020145475:AAGhhEUrn3F9t_wWzbX68u7PF_P6DcjPHxc"
TELEGRAM_CHAT_ID = "5909474475"

def send_telegram_message(message: str):
    """
    Sends a formatted message to your Telegram chat using bot API.
    """
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, data=payload)
        if response.status_code != 200:
            print(f"[Telegram Error] Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[Telegram Error] {e}")

def expert_trade_suggestion(price, support, resistance, signal):
    """
    Generates expert trading suggestion based on price, S/R levels, and signal type.
    """
    try:
        price = float(price)
        support = float(support)
        resistance = float(resistance)

        if signal == "Scalping":
            if price <= support:
                return "Scalp Buy: near support"
            elif price >= resistance:
                return "Scalp Sell: near resistance"
            else:
                return "Scalp Zone: Watch closely"
        
        elif signal == "Long":
            if price <= support:
                return "Long Entry: near major support"
            elif price >= resistance:
                return "Long TP: near resistance"
            else:
                return "Long Hold: consolidation zone"
        
        elif signal == "Short":
            if price >= resistance:
                return "Short Entry: resistance confirmed"
            elif price <= support:
                return "Short TP: approaching target"
            else:
                return "Short Watch: waiting signal"
        
        else:
            return "No clear signal"
    except Exception as e:
        return f"Expert Error: {e}"