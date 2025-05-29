import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_mini_chart(prices: list, symbol: str = "") -> str:
    """
    Generates a small price trend chart as base64-encoded image.
    Returns a string that can be embedded in Streamlit.
    """
    if not prices or len(prices) < 2:
        return ""

    fig, ax = plt.subplots(figsize=(2.5, 0.75))
    ax.plot(prices, linewidth=1.2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(symbol, fontsize=6)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # Save image to buffer
    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0.05)
    plt.close(fig)
    buf.seek(0)

    # Encode image to base64
    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return f"<img src='data:image/png;base64,{image_base64}' width='100'/>"