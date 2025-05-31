import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import MaxNLocator
import pandas as pd
from io import BytesIO
import base64

def generate_expert_chart(df, symbol):
    # Ensure datetime index
    df = df.copy()
    df.index = pd.to_datetime(df.index)

    # Plotting setup
    fig = plt.figure(figsize=(6, 5))
    ax_price = plt.subplot2grid((5, 1), (0, 0), rowspan=3)
    ax_rsi = plt.subplot2grid((5, 1), (3, 0), rowspan=1)
    ax_vol = plt.subplot2grid((5, 1), (4, 0), rowspan=1)

    # Candlestick chart
    ohlc = df[['open', 'high', 'low', 'close']].copy()
    candle_colors = df['close'] > df['open']
    ax_price.bar(df.index, df['high'] - df['low'], bottom=df['low'], color='gray', linewidth=0.5)
    ax_price.bar(df.index, df['close'] - df['open'], bottom=df['open'],
                 color=candle_colors.map({True: 'green', False: 'red'}), width=0.0015)

    # EMA lines
    ax_price.plot(df.index, df['EMA9'], label='EMA9', linestyle='--')
    ax_price.plot(df.index, df['EMA21'], label='EMA21', linestyle='-.')

    # Support & Resistance (last 10 candles)
    support = min(df['low'][-10:])
    resistance = max(df['high'][-10:])
    ax_price.axhline(support, color='blue', linestyle='--', linewidth=1, label='Support')
    ax_price.axhline(resistance, color='orange', linestyle='--', linewidth=1, label='Resistance')

    ax_price.set_title(f"{symbol} Expert Chart")
    ax_price.legend(loc="upper left")
    ax_price.grid(True)

    # RSI plot
    ax_rsi.plot(df.index, df['RSI'], color='purple')
    ax_rsi.axhline(70, color='red', linestyle='--', linewidth=0.8)
    ax_rsi.axhline(30, color='green', linestyle='--', linewidth=0.8)
    ax_rsi.set_ylabel("RSI")
    ax_rsi.grid(True)

    # Volume bars
    ax_vol.bar(df.index, df['volume'], color='skyblue')
    ax_vol.set_ylabel("Volume")
    ax_vol.grid(True)

    # Formatting
    for ax in [ax_price, ax_rsi, ax_vol]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()

    # Encode to base64
    buf = BytesIO()
    plt.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode("utf-8")