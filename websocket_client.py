import threading
import websocket
import json
import time

# Global dictionary to store live prices
live_prices = {}

# List of tracked symbols (Coinbase format)
tracked_symbols = [
    'BTC-USD', 'ETH-USD', 'SOL-USD', 'AVAX-USD', 'LTC-USD',
    'ADA-USD', 'DOGE-USD', 'PEPE-USD', 'SHIB-USD'
]

def on_message(ws, message):
    try:
        data = json.loads(message)
        if 'type' in data and data['type'] == 'ticker':
            symbol = data['product_id']
            price = float(data['price'])
            coin = symbol.split('-')[0]
            live_prices[coin] = price
    except Exception as e:
        print(f"[WebSocket Error] Message handling failed: {e}")

def on_error(ws, error):
    print(f"[WebSocket Error] {error}")

def on_close(ws, close_status_code, close_msg):
    print("[WebSocket] Connection closed")

def on_open(ws):
    try:
        subscribe_msg = {
            "type": "subscribe",
            "channels": [{"name": "ticker", "product_ids": tracked_symbols}]
        }
        ws.send(json.dumps(subscribe_msg))
    except Exception as e:
        print(f"[WebSocket Error] Failed to subscribe: {e}")

def start_websocket():
    while True:
        try:
            ws = websocket.WebSocketApp(
                "wss://ws-feed.exchange.coinbase.com",
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.run_forever()
        except Exception as e:
            print(f"[WebSocket Error] Connection failed, retrying in 5s: {e}")
            time.sleep(5)

def start_websocket_thread():
    thread = threading.Thread(target=start_websocket)
    thread.daemon = True
    thread.start()