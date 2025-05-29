
import streamlit as st
import requests
import time

def app():
    st.title("🟢 Ready to Trade")

    symbol = st.selectbox("Select Coin", ["BTC", "ETH"])
    entry = st.number_input("Entry Price", min_value=0.0, format="%.2f")
    stop_loss = st.number_input("Stop Loss", min_value=0.0, format="%.2f")
    take_profit = st.number_input("Take Profit", min_value=0.0, format="%.2f")

    if st.button("Activate Trade Monitor"):
        if entry > 0 and stop_loss > 0 and take_profit > 0:
            st.session_state[f"{symbol}_trade"] = {
                'entry': entry,
                'stop_loss': stop_loss,
                'take_profit': take_profit,
                'start_time': time.time()
            }
            st.success(f"🔔 {symbol} trade monitor activated!")
        else:
            st.warning("Please complete all fields.")
