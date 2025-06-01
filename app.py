# app.py – Final clean version with real-time price and public OHLCV (no refresh errors)
import streamlit as st
st.set_page_config(layout="wide")  # ✅ First Streamlit command

# ✅ Auto-refresh every 5 seconds using HTML meta tag
st.markdown("<meta http-equiv='refresh' content='5'>", unsafe_allow_html=True)

import pandas as pd
from signal_engine import generate_all_signals
from plot_chart import generate_yanto_chart
from websocket_client import get_latest_price
from ohlcv_data import get_ohlcv

st.title("📡 Nobu AI Terminal Pro – Yanto Bubut Scalping Edition")

# Top 10 coins for scalping
coins = ['BTC-USD', 'ETH-USD', 'PEPE-USD', 'DOGE-USD', 'ADA-USD',
         'SOL-USD', 'AVAX-USD', 'LINK-USD', 'MATIC-USD', 'OP-USD']

# Generate signal table using WebSocket prices
df = generate_all_signals(coins)
st.dataframe(df)

# Chart section
selected_symbol = st.selectbox("Select a coin to view chart:", df["Symbol"])

try:
    chart_df = get_ohlcv(selected_symbol, granularity=60)
    chart_df["EMA9"] = chart_df["close"].ewm(span=9).mean()
    chart_df["EMA21"] = chart_df["close"].ewm(span=21).mean()
    chart_df.rename(columns={"time": "Time", "close": "Close"}, inplace=True)

    row = df[df["Symbol"] == selected_symbol].iloc[0]
    support = row["Support"]
    sl = row["SL"]
    tp = row["TP"]
    live_price = row["Price"] or get_latest_price(selected_symbol)

    chart_base64 = generate_yanto_chart(chart_df, support, sl, tp, live_price)
    st.markdown(f"![chart](data:image/png;base64,{chart_base64})")

except Exception as e:
    st.error(f"Error fetching OHLCV data: {e}")
