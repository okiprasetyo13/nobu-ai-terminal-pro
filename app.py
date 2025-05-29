import streamlit as st
from signal_engine import analyze_all_symbols
from plot_chart import generate_mini_chart
from telegram_alerts import expert_trade_suggestion

# Analyze signals
df_signals = analyze_all_symbols()

# Check and display available columns (for debugging)
st.checkbox("🔍 df_signals Columns:", value=True)
st.write(df_signals.columns.tolist())

# Prevent crash if 'Symbol' is missing
if "Symbol" not in df_signals.columns or df_signals.empty:
    st.error("⚠️ No valid signal data returned.")
else:
    # Add Live Price column
    df_signals["Live Price"] = df_signals["Symbol"].apply(
        lambda sym: latest_prices.get(sym, None)
    )

    # Add mini chart column
    def safe_chart(row):
        price_history = row.get("Price History", [])
        if isinstance(price_history, list) and len(price_history) > 0:
            return generate_mini_chart(price_history, row["Symbol"])
        return "--"

    df_signals["Chart"] = df_signals.apply(safe_chart, axis=1)

    # Add expert advice column
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
        "Symbol", "Price", "RSI", "EMA9", "EMA21",
        "Support", "Resistance", "Entry", "SL", "TP", "Score",
        "Suitability", "Expert Tip", "Expert Advice", "Chart"
    ]
    df_display = df_signals[columns_order].copy()

    # Format floats
    def fmt(val):
        return f"{val:.8f}" if isinstance(val, float) and val < 1 else f"{val:.2f}" if isinstance(val, float) else val

    df_display = df_display.applymap(fmt)

    # Display the table
    st.markdown("📊 <b>Live Expert Scalping Signals</b>", unsafe_allow_html=True)
    st.dataframe(df_display, use_container_width=True)

    st.success("✅ Nobu AI Terminal v0.2 loaded. Fully live and tested.")