import matplotlib.pyplot as plt
import base64
from io import BytesIO

def generate_chart_base64(df):
    try:
        fig, ax = plt.subplots(figsize=(2.5, 1.2))
        ax.plot(df['close'], linewidth=1.5)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off')
        plt.tight_layout()

        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=100, bbox_inches='tight', pad_inches=0)
        plt.close(fig)
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode('utf-8')
        return f'<img src="data:image/png;base64,{image_base64}" width="80"/>'
    except Exception as e:
        return "<i>Chart error</i>"

