# app.py (Production - Nobu AI Terminal Pro + Yanto Bubut Patch)
import streamlit as st
import pandas as pd
from signal_engine import generate_all_signals
from plot_chart import generate_yanto_chart

st.set_page_config(layout="wide")
st.title("📡 Nobu AI Terminal Pro – Yanto Bubut Scalping Edition")

coins = ['BTC', 'ETH', 'PEPE', 'DOGE', 'ADA', 'SOL', 'AVAX', 'LINK', 'MATIC', 'OP']

def price_fetcher(symbol):
    import random
    return round(random.uniform(0.000001, 200), 8)

df = generate_all_signals(coins, price_fetcher)
st.dataframe(df)

selected_symbol = st.selectbox("Select a coin to view chart:", df["Symbol"])
chart_df = pd.DataFrame({
    "Time": pd.date_range(end=pd.Timestamp.now(), periods=60, freq='min'),
    "Close": [price_fetcher(selected_symbol) for _ in range(60)],
})
chart_df["EMA9"] = chart_df["Close"].ewm(span=9).mean()
chart_df["EMA21"] = chart_df["Close"].ewm(span=21).mean()

row = df[df["Symbol"] == selected_symbol].iloc[0]
if row["Price"] is not None and row["SL"] is not None and row["TP"] is not None:
    chart_base64 = generate_yanto_chart(chart_df, row["Support"], row["SL"], row["TP"], row["Price"])
    st.markdown(f"![chart](data:image/png;base64,{chart_base64})")
else:
    st.warning("No valid buy signal yet for this coin — chart lines disabled.")
