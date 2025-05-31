import matplotlib.pyplot as plt
import pandas as pd
from ta.trend import EMAIndicator, MACD
from io import BytesIO
import base64

def generate_expert_chart(price_history, symbol):
    # 🔒 Ensure DataFrame structure
    if isinstance(price_history, list):
        df = pd.DataFrame(price_history, columns=["close"])
    elif isinstance(price_history, pd.Series):
        df = price_history.to_frame(name="close")
    else:
        df = price_history.copy()

    # Simulate OHLCV structure for plotting
    df["open"] = df["close"].shift(1).fillna(method="bfill")
    df["high"] = df["close"] + 2
    df["low"] = df["close"] - 2
    df["Volume"] = 10000

    df["EMA9"] = EMAIndicator(df["close"], window=9).ema_indicator()
    df["EMA21"] = EMAIndicator(df["close"], window=21).ema_indicator()

    macd = MACD(df["close"])
    df["MACD"] = macd.macd()
    df["MACD_SIGNAL"] = macd.macd_signal()

    df.index = pd.date_range(end=pd.Timestamp.now(), periods=len(df), freq="1min")

    # === 🎯 Charting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 5), sharex=True, height_ratios=[3, 1])

    # 📈 Price panel
    ax1.plot(df.index, df["close"], label="Price", color="blue", linewidth=2)
    ax1.plot(df.index, df["EMA9"], label="EMA9", linestyle="--", color="orange")
    ax1.plot(df.index, df["EMA21"], label="EMA21", linestyle="--", color="purple")
    ax1.fill_between(df.index, df["low"], df["high"], color="gray", alpha=0.2, label="Range")
    ax1.axhline(df["close"].iloc[-1] + 5, color="green", linestyle="--", label="TP")
    ax1.axhline(df["close"].iloc[-1] - 5, color="red", linestyle="--", label="SL")
    ax1.set_title(f"{symbol} – Price + EMA + TP/SL")
    ax1.legend()
    ax1.grid(True)

    # 📉 MACD panel
    ax2.plot(df.index, df["MACD"], label="MACD", color="teal")
    ax2.plot(df.index, df["MACD_SIGNAL"], label="Signal", linestyle="--", color="red")
    ax2.axhline(0, linestyle=":", color="gray")
    ax2.set_title("MACD Indicator")
    ax2.legend()
    ax2.grid(True)

    plt.tight_layout()

    # 🧪 Convert to base64
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    return img_base64