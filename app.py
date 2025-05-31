import streamlit as st
import pandas as pd
from signal_engine import generate_all_signals
from plot_chart import generate_mini_chart
from websocket_client import start_websocket_client
from ready_to_trade import get_ready_to_trade_data

st.set_page_config(page_title="Nobu AI Terminal Pro v0.2", layout="wide")

# Start WebSocket client in the background
start_websocket_client()

st.title("📡 Nobu AI Terminal Pro – Expert Scalping Terminal v0.2")

# Live Scalping Signal Table
st.subheader("📈 Live Scalping Signal Table (Real-Time)")
signal_data = generate_all_signals()
# 🧠 Expert One-Glance Signal Table
st.subheader("📊 Expert Signal Table (One-Glance View)")

# Headers
cols = st.columns([1.1, 1.1, 1, 1, 1, 1.3, 1.1, 1.1, 1.8, 2.5])
headers = [
    "Symbol", "Strategy", "RSI", "Score", "Signal",
    "Price", "TP", "SL", "Advice", "Chart"
]
for col, header in zip(cols, headers):
    col.markdown(f"**{header}**")

# Rows
for _, row in signal_data.iterrows():
    chart = generate_mini_chart(row["Price History"])

    cols = st.columns([1.1, 1.1, 1, 1, 1, 1.3, 1.1, 1.1, 1.8, 2.5])
    cols[0].markdown(f"🪙 {row['Symbol']}")
    cols[1].markdown(f"`{row['Strategy']}`")
    cols[2].markdown(f"{row['RSI']:.2f}")
    cols[3].markdown(f"🧠 {row['Score']}")
    cols[4].markdown(f"`{row['Signal']}`")
    cols[5].markdown(f"${row['Current Price']:.2f}")
    cols[6].markdown(f"{row['Take Profit']}")
    cols[7].markdown(f"{row['Stop Loss']}")
    cols[8].markdown(f"📌 *{row['Advice']}*")
    cols[9].image(chart, use_column_width=True)
            
# Ready to Trade Panel
st.subheader("✅ Ready to Trade Now (Top Opportunities)")
ready_data = get_ready_to_trade_data()
if not ready_data.empty:
    st.dataframe(ready_data, use_container_width=True)
else:
    st.info("No ready-to-trade coins identified at this time.")

# Footer
st.markdown("---")
st.caption("Nobu AI Terminal Pro v0.2 – Tested and Verified • Built for Real Scalping Profits ⚡")