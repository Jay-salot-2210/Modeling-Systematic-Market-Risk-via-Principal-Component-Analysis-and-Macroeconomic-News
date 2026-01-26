import streamlit as st
import pandas as pd
import os

st.set_page_config(
    page_title="Market Risk Monitor (PC1)",
    page_icon="📉",
    layout="centered"
)

st.title("📊 Systematic Market Risk Dashboard")
st.caption("Live PC1 market mode prediction using global news")

DATA_PATH = "data/daily_pc1_dashboard.csv"

if not os.path.exists(DATA_PATH):
    st.warning("⏳ No daily prediction data available yet.")
    st.info(
        "The dashboard will automatically update once the daily "
        "GitHub Actions pipeline runs and commits data."
    )
    st.stop()

df = pd.read_csv("data/daily_pc1_dashboard.csv")

latest = df.iloc[-1]

direction = "Risk-On 📈" if latest["pc1_probability"] >= 0.5 else "Risk-Off 📉"

col1, col2 = st.columns(2)
col1.metric("Market Regime", direction)
col2.metric("PC1 Probability", f"{latest['pc1_probability']:.2%}")

st.divider()

st.subheader("🔍 What drove today's prediction?")
explain = df[df["date"] == latest["date"]][
    ["feature", "contribution"]
].set_index("feature")

st.bar_chart(explain)

st.divider()

st.subheader("📈 PC1 Risk Trend")
trend = df.groupby("date")["pc1_probability"].mean()
st.line_chart(trend)

st.caption("Updated daily via GitHub Actions")
