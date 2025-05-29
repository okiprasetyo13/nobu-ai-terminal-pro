import streamlit as st
import pandas as pd
from websocket_client import start_price_feed, latest_prices
from signal_engine import generate_signals
from plot_chart import generate_mini_chart
from ready_to_trade import expert_trade_suggestion

# Streamlit page setup
st.set_page_config(page_title="Nobu AI Terminal Pro", layout="wide")
st.title("📡 Nobu AI Terminal Pro – Expert Scalping Signals")

# Initialize WebSocket feed (runs in thread)
start_price_feed()

# Load signal table
with st.spinner("Generating expert scalping signals..."):
    df_signals = generate_signals()

# Append real-time price
df_signals["Live Price"] = df_signals["Symbol"].apply(lambda sym: latest_prices.get(sym, None))

# Add inline chart
df_signals["Chart"] = df_signals["Symbol"].apply(
    lambda sym: generate_mini_chart(df_signals[df_signals["Symbol"] == sym]["Price History"].values[0], sym)
    if "Price History" in df_signals.columns else ""
)

# Add expert advice
df_signals["Expert Advice"] = df_signals.apply(
    lambda row: expert_trade_suggestion(
        price=row["Live Price"],
        support=row["Support"],
        resistance=row["Resistance"],
        signal=row["Signal"]
    ),
    axis=1
)

# Clean up and reorder columns
columns_order = [
    "Symbol", "Live Price", "Signal", "Score", "RSI", "EMA9", "EMA21",
    "Support", "Resistance", "Buy Price", "SL", "TP", "Expert Advice", "Chart"
]
df_display = df_signals[columns_order].copy()

# Format floats for display
def fmt(val):
    return f"{val:.8f}" if isinstance(val, float) and val < 1 else f"{val:.4f}" if isinstance(val, float) else val

df_display = df_display.applymap(fmt)

# Display the table
st.markdown("### 📈 Live Expert Scalping Signals")
st.write(
    df_display.to_html(escape=False, index=False), unsafe_allow_html=True
)

# Footer
st.markdown("---")
st.caption("Built with ❤️ by Nobu AI | v0.2 – Real-time crypto scalping intelligence.")