import requests

# --- Telegram Credentials (Use your actual bot token and chat ID) ---
TELEGRAM_BOT_TOKEN = "8020145475:AAGhhEUrn3F9t_wWzbX68u7PF_P6DcjPHxc"
TELEGRAM_CHAT_ID = "5909474475"

def send_telegram_message(message: str):
    """
    Sends a formatted message to a Telegram chat using the bot API.
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