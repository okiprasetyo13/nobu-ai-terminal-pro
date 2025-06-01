# plot_chart.py (Updated for Conditional SL/TP Lines)
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_yanto_chart(df, support, sl, tp, live_price):
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df['Time'], df['Close'], label='Price', linewidth=1.5)
    ax.plot(df['Time'], df['EMA9'], label='EMA9', linestyle='--')
    ax.plot(df['Time'], df['EMA21'], label='EMA21', linestyle='--')
    ax.axhline(y=support, color='blue', linestyle='-', label='Support')

    if sl is not None:
        ax.axhline(y=sl, color='red', linestyle='--', label='Stop Loss')
    if tp is not None:
        ax.axhline(y=tp, color='green', linestyle='--', label='Take Profit')

    if live_price is not None:
        ax.axhline(y=live_price, color='black', linestyle=':', label='Live Price')

    ax.legend()
    ax.set_title("Yanto Bubut Chart")
    buf = BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format="png")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()