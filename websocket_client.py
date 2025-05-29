import websocket
import json
import threading
import time

# Shared dictionary to store the latest prices
latest_prices = {}

# Coinbase WebSocket endpoint
SOCKET = "wss://ws-feed.exchange.coinbase.com"

# List of symbols to subscribe (USD pairs only)
SYMBOLS = [
    "BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "LTC-USD",
    "OP-USD", "INJ-USD", "PEPE-USD", "DOGE-USD", "ADA-USD",
    "MATIC-USD", "BCH-USD", "DOT-USD", "RNDR-USD", "AR-USD",
    "TON-USD", "WCFG-USD", "WLD-USD", "SUI-USD", "BONK-USD"
]

def get_latest_price(symbol):
    return latest_prices.get(symbol)

def on_open(ws):
    print("WebSocket connection opened.")
    subscribe_message = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": SYMBOLS}]
    }
    ws.send(json.dumps(subscribe_message))

def on_message(ws, message):
    try:
        msg = json.loads(message)
        if msg.get("type") == "ticker" and "product_id" in msg and "price" in msg:
            product_id = msg["product_id"]
            price = float(msg["price"])
            latest_prices[product_id] = price
    except Exception as e:
        print(f"WebSocket message error: {e}")

def on_error(ws, error):
    print(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")

def start_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp(
                SOCKET,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        except Exception as e:
            print(f"WebSocket connection failed: {e}")
            time.sleep(5)  # Retry after 5 seconds

# Start WebSocket in a background thread
def launch_websocket_thread():
    thread = threading.Thread(target=start_websocket)
    thread.daemon = True
    thread.start()