import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_mini_chart(price_history, symbol):
    """
    Generates a base64 inline chart for a given price history list.
    """
    try:
        fig, ax = plt.subplots(figsize=(2, 0.8))
        ax.plot(price_history, linewidth=1.5)
        ax.set_title(symbol, fontsize=6)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("white")
        plt.tight_layout()

        # Save figure to base64
        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=100)
        plt.close(fig)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
        return f'<img src="data:image/png;base64,{image_base64}" width="120"/>'
    except Exception as e:
        print(f"[Chart Error] {symbol}: {e}")
        return "--"