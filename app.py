import streamlit as st
import pandas as pd
from signal_engine import generate_signals
from plot_chart import generate_mini_chart
from websocket_client import start_websocket_client
from ready_to_trade import get_ready_to_trade_data

st.set_page_config(page_title="Nobu AI Terminal Pro v0.2", layout="wide")

# Start WebSocket client in the background
start_websocket_client()

st.title("📡 Nobu AI Terminal Pro – Expert Scalping Terminal v0.2")

# Live Scalping Signal Table
st.subheader("📈 Live Scalping Signal Table (Real-Time)")
signal_data = generate_signals()
if not signal_data.empty:
    for idx, row in signal_data.iterrows():
        with st.container():
            col1, col2 = st.columns([2, 5])
            with col1:
                st.markdown(f"**{row['Symbol']} – ${row['Current Price']:.8f}**")
                st.markdown(f"RSI: {row['RSI']:.2f}")
                st.markdown(f"Signal: `{row['Signal']}`")
                st.markdown(f"Score: {row['Score']}")
                st.markdown(f"Support: {row['Support']}")
                st.markdown(f"Resistance: {row['Resistance']}")
                st.markdown(f"Buy Price: {row['Buy Price']}")
                st.markdown(f"TP: {row['Take Profit']} | SL: {row['Stop Loss']}")
                st.markdown(f"Strategy: `{row['Strategy']}`")
                st.markdown(f"Advice: 📌 _{row['Advice']}_")
            with col2:
                st.image(
                generate_mini_chart(row["Price History"], row["Symbol"]),
                caption="Mini Chart",
                use_column_width=True
                )

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