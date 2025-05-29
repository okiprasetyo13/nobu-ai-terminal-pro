import streamlit as st
import pandas as pd
from signal_engine import generate_signals
from websocket_client import get_latest_prices
from ready_to_trade import evaluate_trade_opportunities
from plot_chart import generate_chart_image
from telegram_alerts import send_telegram_alert

# --- Streamlit Setup ---
st.set_page_config(page_title="Nobu AI Terminal Pro", layout="wide")
st.title("📡 Nobu AI Terminal Pro – Live Expert Scalping Signal")

# --- Load Signals and Data ---
with st.spinner("Loading market data and signals..."):
    live_prices = get_latest_prices()
    signal_data = generate_signals(live_prices)
    trade_advice = evaluate_trade_opportunities(signal_data)

# --- Display Table ---
st.subheader("💹 Live Scalping Signals – Updated in Real Time")

if signal_data.empty:
    st.warning("No signal data available. Please wait for updates.")
else:
    for i, row in signal_data.iterrows():
        col1, col2 = st.columns([3, 2])
        with col1:
            st.markdown(f"### {row['Symbol']} - ${row['Current Price']}")
            st.metric("Score", row['Signal Score'], delta=None)
            st.write(f"**Buy Price:** {row['Buy Price']}")
            st.write(f"**Support:** {row['Support']} | **Resistance:** {row['Resistance']}")
            st.write(f"**SL:** {row['SL']} | **TP:** {row['TP']}")
            st.write(f"**RSI:** {row['RSI']} | **EMA(9):** {row['EMA9']} | **EMA(21):** {row['EMA21']}")
            st.write(f"**Volume:** {row['Volume']}")

        with col2:
            st.image(generate_chart_image(row['Symbol']), caption="Live Chart", use_column_width=True)

        st.success(f"**Expert Advice:** {row['Expert Advice']}")

# --- Alert Section ---
st.markdown("---")
st.subheader("📬 SL/TP Alert Test (Manual Trigger)")
if st.button("Test Telegram Alert"):
    send_telegram_alert("Test alert from Nobu AI Terminal 🚀")
    st.success("Test alert sent.")