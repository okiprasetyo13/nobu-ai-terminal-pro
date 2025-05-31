import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_mini_chart(prices, support=None, resistance=None):
    """
    Generates a mini inline chart for display in the Signal Table.
    :param prices: List of recent closing prices
    :param support: Optional support level line
    :param resistance: Optional resistance level line
    :return: Base64 image string
    """
    fig, ax = plt.subplots(figsize=(3, 1))
    ax.plot(prices, linewidth=1.5)

    # Optional support/resistance lines
    if support:
        ax.axhline(support, color='green', linestyle='--', linewidth=0.5)
    if resistance:
        ax.axhline(resistance, color='red', linestyle='--', linewidth=0.5)

    ax.axis('off')
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode()
    plt.close(fig)

    # ✅ Streamlit expects a raw base64 string, not <img> HTML
    return f"data:image/png;base64,{image_base64}"