import threading
import websocket
import json

# Store live prices
latest_prices = {}

def on_message(ws, message):
    data = json.loads(message)
    if "price" in data:
        symbol = data["product_id"].replace("-USDT", "")
        latest_prices[symbol] = float(data["price"])

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws):
    print("WebSocket closed")

def start_price_feed():
    def run():
        ws = websocket.WebSocketApp(
            "wss://ws-feed.exchange.coinbase.com",
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        ws.on_open = lambda ws: ws.send(json.dumps({
            "type": "subscribe",
            "channels": [{
                "name": "ticker",
                "product_ids": [f"{coin}-USDT" for coin in [
                    "BTC", "ETH", "PEPE", "AVAX", "LTC", "MATIC", "ARB", "RNDR",
                    "OP", "ADA", "INJ", "SUI", "DOGE", "XRP", "BLUR", "DYDX",
                    "APT", "SOL", "DOT", "IMX"
                ]]
            }]
        }))
        ws.run_forever()

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()