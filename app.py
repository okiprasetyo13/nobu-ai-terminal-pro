import streamlit as st
import pandas as pd
from signal_engine import analyze_all_symbols
from plot_chart import generate_chart_base64
from telegram_alerts import expert_trade_suggestion
from websocket_client import latest_prices

st.set_page_config(page_title="Nobu AI Terminal Pro", layout="wide")
st.title("📡 Nobu AI Terminal Pro – Expert Scalping Signals")

# Analyze signals
df_signals = analyze_all_symbols()

# Check and display available columns (for debug)
st.checkbox("🔍 df_signals Columns:", value=True)
st.write(df_signals.columns.tolist())

# Prevent crash if 'Symbol' is missing
if "Symbol" not in df_signals.columns or df_signals.empty:
    st.error("⚠️ No valid signal data returned. Please check your filters or try again later.")
else:
    # Add Live Price column
    df_signals["Live Price"] = df_signals["Symbol"].apply(lambda sym: latest_prices.get(sym, None))

    # Add mini chart column
    df_signals["Chart"] = df_signals["Symbol"].apply(
        lambda sym: generate_chart_base64(df_signals[df_signals["Symbol"] == sym]["Price History"].values[0], sym)
        if "Price History" in df_signals.columns else "--"
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

    # Clean column order
    columns_order = [
        "Symbol", "Price", "RSI", "EMA9", "EMA21",
        "Support", "Resistance", "Entry", "SL", "TP",
        "Score", "Suitability", "Expert Advice", "Chart"
    ]
    df_display = df_signals[columns_order].copy()

    # Format floats
    def fmt(val):
        return f"{val:.8f}" if isinstance(val, float) and val < 1 else f"{val:,.2f}" if isinstance(val, float) else val
    df_display = df_display.applymap(fmt)

    # Display table
    st.subheader("📊 Live Scalping Signal Table")
    st.dataframe(df_display, use_container_width=True, hide_index=True)

    st.success("✅ Full table rendered with live data and charts.")

# Footer
st.markdown("✅ Nobu AI Terminal v0.2 Pro loaded. Live signal engine and charts are integrated.")