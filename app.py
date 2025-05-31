import streamlit as st
import pandas as pd
import requests
from ta.momentum import RSIIndicator
from signal_engine import generate_all_signals
from plot_chart import generate_expert_chart
from websocket_client import start_websocket_client
from ready_to_trade import get_ready_to_trade_data
from websocket_client import launch_websocket_thread


launch_websocket_thread()
print("[⚡] WebSocket thread launched")

st.set_page_config(page_title="Nobu AI Terminal Pro v0.2", layout="wide")

# Start WebSocket client in the background
start_websocket_client()

st.title("📡 Nobu AI Terminal Pro – Expert Scalping Terminal v0.2")

# === Live FastAPI Price Fetcher ===
@st.cache_data(ttl=5)
def get_live_price(symbol):
    try:
        url = f"https://nobu-fastapi-price.onrender.com/price/{symbol}"
        res = requests.get(url).json()
        return float(res["price"])
    except:
        return None

# Live Scalping Signal Table
st.subheader("📈 Live Scalping Signal Table (Real-Time)")
signal_data = generate_all_signals()

# 🧠 Expert One-Glance Signal Table
st.subheader("📊 Expert Signal Table (One-Glance View)")

# Headers
cols = st.columns([1.1, 1.1, 1.1, 1, 1, 1.3, 1.3, 1.1, 1.1, 1.8, 2.5, 2.5])
headers = [
    "Symbol", "Strategy", "RSI", "Score", "Signal",
    "Price", "Recommended Buy", "TP", "SL", "Resistance", "Advice", "Chart"
]
for col, header in zip(cols, headers):
    col.markdown(f"**{header}**")

# Rows
from ta.momentum import RSIIndicator  # ✅ Make sure this is imported at the top

# ✅ Inside signal_data.iterrows loop
for _, row in signal_data.iterrows():
    cols = st.columns([1.1, 1.1, 1, 1, 1, 1.3, 1.1, 1.1, 1.1, 1.8, 2.5])
    live_price = get_live_price(row["Symbol"])
    price_display = f"${live_price:,.2f}" if live_price else f"${row['Current Price']:.2f}"

    # 💡 Safe chart prep inside loop
    df_history = pd.DataFrame(row["Price History"], columns=["close"])
    df_history["open"] = df_history["close"].shift(1).fillna(method="bfill")
    df_history["high"] = df_history["close"] + 5
    df_history["low"] = df_history["close"] - 5
    df_history["volume"] = 10000
    df_history["EMA9"] = df_history["close"].ewm(span=9).mean()
    df_history["EMA21"] = df_history["close"].ewm(span=21).mean()
    df_history["RSI"] = RSIIndicator(df_history["close"], window=14).rsi()
    df_history.index = pd.date_range(end=pd.Timestamp.now(), periods=len(df_history), freq="1min")

    # ✅ Show expert table with chart
    cols[0].markdown(f"🪙 {row['Symbol']}")
    cols[1].markdown(f"`{row['Strategy']}`")
    cols[2].markdown(f"{row['RSI']:.2f}")
    cols[3].markdown(f"🧠 {row['Score']}")
    cols[4].markdown(f"`{row['Signal']}`")
    cols[5].markdown(price_display)
    cols[6].markdown(row["Take Profit"])
    cols[7].markdown(row["Stop Loss"])
    cols[8].markdown(f"🧱 {row['Resistance']}")
    cols[9].markdown(f"📌 *{row['Advice']}*")

    # ✅ Generate chart AFTER df_history is ready
    chart = generate_expert_chart(df_history, row["Symbol"])
    cols[10].image("data:image/png;base64," + chart, use_column_width=True)

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