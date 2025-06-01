# app.py (Updated for Always Visible Chart)
import streamlit as st
import pandas as pd
from signal_engine import generate_all_signals
from plot_chart import generate_yanto_chart

st.set_page_config(layout="wide")
st.title("📡 Nobu AI Terminal Pro – Yanto Bubut Scalping Edition")

# Coin list
coins = ['BTC', 'ETH', 'PEPE', 'DOGE', 'ADA', 'SOL', 'AVAX', 'LINK', 'MATIC', 'OP']

# Placeholder live price fetcher (replace with get_latest_price for real)
def price_fetcher(symbol):
    import random
    return round(random.uniform(0.000001, 200), 8)

# Generate signal table
df = generate_all_signals(coins, price_fetcher)
st.dataframe(df)

# Select coin
selected_symbol = st.selectbox("Select a coin to view chart:", df["Symbol"])
chart_df = pd.DataFrame({
    "Time": pd.date_range(end=pd.Timestamp.now(), periods=60, freq='min'),
    "Close": [price_fetcher(selected_symbol) for _ in range(60)],
})
chart_df["EMA9"] = chart_df["Close"].ewm(span=9).mean()
chart_df["EMA21"] = chart_df["Close"].ewm(span=21).mean()

# Get row data
row = df[df["Symbol"] == selected_symbol].iloc[0]
support = row["Support"]
sl = row["SL"]
tp = row["TP"]
live_price = row["Price"] or price_fetcher(selected_symbol)

# Generate chart
chart_base64 = generate_yanto_chart(chart_df, support, sl, tp, live_price)
st.markdown(f"![chart](data:image/png;base64,{chart_base64})")