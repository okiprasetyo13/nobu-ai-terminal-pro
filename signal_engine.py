def generate_all_signals():
    import pandas as pd
    import random

    signal_rows = []

    symbol_list = [
        'BTC', 'ETH', 'SOL', 'APT', 'AVAX', 'OP', 'ARB', 'PEPE', 'DOGE', 'LTC',
        'MATIC', 'SUI', 'INJ', 'LINK', 'RNDR', 'WIF', 'BLUR', 'SHIB', 'TIA', 'JUP'
    ]

    for symbol in symbol_list:
        try:
            # Generate a base price per symbol
            coinbase_symbol = f"{symbol}-USD"
            base_price = get_live_price(symbol)
            print(f"[🔄] {symbol} live price = {base_price}")
            price_history = [base_price + random.randint(-200, 200) for _ in range(10)]

            row = {
                'Symbol': symbol,
                'Strategy': 'Scalping',
                'Score': random.randint(3, 5),
                'Buy Price': base_price,
                'Take Profit': base_price + 500,
                'Stop Loss': base_price - 500,
                'Support': base_price - 300,
                'Resistance': base_price + 700,
                'Current Price': base_price,
                'Signal': 'Buy',
                'RSI': round(random.uniform(25, 40), 2),
                'EMA9': base_price - 50,
                'EMA21': base_price - 100,
                'Volume': random.randint(1000000, 50000000),
                'Advice': 'Buy on support',
                'Trade Type': 'Scalping',
                'Price History': price_history,
            }

            signal_rows.append(row)
            print(f"[✅] Signal added for {symbol}")

        except Exception as e:
            print(f"[❌] Error processing {symbol}: {e}")

    return pd.DataFrame(signal_rows)