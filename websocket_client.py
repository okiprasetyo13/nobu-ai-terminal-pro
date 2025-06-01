# websocket_client.py – Live Price Fetcher from Coinbase WebSocket (No API key)
import websocket
import threading
import json

# Dictionary to store latest prices per symbol
latest_prices = {}

# List of symbols to subscribe (Coinbase format)
symbols_to_subscribe = ["BTC-USD", "ETH-USD", "PEPE-USD", "DOGE-USD", "ADA-USD",
                        "SOL-USD", "AVAX-USD", "LINK-USD", "MATIC-USD", "OP-USD"]

def on_message(ws, message):
    global latest_prices
    data = json.loads(message)
    if data.get("type") == "ticker":
        product_id = data.get("product_id")
        price = float(data.get("price", 0))
        latest_prices[product_id] = price

def on_open(ws):
    subscribe_msg = {
        "type": "subscribe",
        "channels": [{"name": "ticker", "product_ids": symbols_to_subscribe}]
    }
    ws.send(json.dumps(subscribe_msg))

def start_websocket():
    url = "wss://ws-feed.exchange.coinbase.com"
    ws = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message)
    ws.run_forever()

# Start WebSocket in a background thread
threading.Thread(target=start_websocket, daemon=True).start()

# Public function to get latest price
def get_latest_price(symbol: str):
    return latest_prices.get(symbol.upper())
