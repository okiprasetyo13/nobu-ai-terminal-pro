import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_chart_base64(df, symbol=""):
    """
    Generate a mini inline chart and return it as a base64-encoded image for embedding in Streamlit table.
    """
    if df is None or df.empty:
        return ""

    try:
        fig, ax = plt.subplots(figsize=(2, 1))
        ax.plot(df["close"].values[-30:], linewidth=1.5, color='blue')
        ax.set_title(symbol, fontsize=6)
        ax.axis('off')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)

        image_base64 = base64.b64encode(buf.read()).decode()
        return f'<img src="data:image/png;base64,{image_base64}" width="80" height="30" />'
    except Exception as e:
        print(f"[Chart error] {e}")
        return ""