import streamlit as st
import plotly.express as px

from src.loader import load_heat_predictions
from src.utils import page_title, footer, download_csv
from src.charts import (
    heat_risk_distribution,
    heat_gauge
)

# ============================================
# Load Data
# ============================================

df = load_heat_predictions()

page_title(
    "🔥 Heat Risk Assessment",
    "Urban Heat Risk Analysis & Monitoring"
)

if df.empty:
    st.error("heat_risk_predictions.csv not found in outputs folder.")
    st.stop()

# ============================================
# KPI Cards
# ============================================

low = (df["Heat Risk"] == "Low").sum()
moderate = (df["Heat Risk"] == "Moderate").sum()
high = (df["Heat Risk"] == "High").sum()
extreme = (df["Heat Risk"] == "Extreme").sum()

avg_score = df["Heat Risk Score"].mean()
avg_temp = df["Predicted Temperature"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("🟢 Low", low)
c2.metric("🟡 Moderate", moderate)
c3.metric("🟠 High", high)
c4.metric("🔴 Extreme", extreme)
c5.metric("🌡 Avg Heat Score", f"{avg_score:.1f}")

st.divider()

# ============================================
# Gauge Chart
# ============================================

st.subheader("Overall Heat Risk Score")

fig = heat_gauge(avg_score)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ============================================
# Risk Distribution
# ============================================

left, right = st.columns(2)

with left:

    st.subheader("Heat Risk Distribution")

    fig = heat_risk_distribution(df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Heat Risk Percentage")

    risk_percent = (
        df["Heat Risk"]
        .value_counts(normalize=True)
        .reset_index()
    )

    risk_percent.columns = [
        "Heat Risk",
        "Percentage"
    ]

    risk_percent["Percentage"] *= 100

    fig = px.pie(
        risk_percent,
        names="Heat Risk",
        values="Percentage",
        hole=0.45,
        color="Heat Risk",
        color_discrete_map={
            "Low": "green",
            "Moderate": "gold",
            "High": "orange",
            "Extreme": "red"
        },
        title="Heat Risk Percentage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ============================================
# Heat Score Histogram
# ============================================

st.subheader("Heat Risk Score Distribution")

fig = px.histogram(
    df,
    x="Heat Risk Score",
    nbins=25,
    color="Heat Risk",
    template="plotly_white",
    title="Heat Risk Score Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ============================================
# Top High-Risk Cities
# ============================================

st.subheader("Top 20 Highest Heat Risk Areas")

top20 = df.sort_values(
    by="Heat Risk Score",
    ascending=False
).head(20)

st.dataframe(
    top20,
    use_container_width=True,
    hide_index=True
)

st.divider()

# ============================================
# Predicted Temperature vs Heat Risk
# ============================================

st.subheader("Predicted Temperature vs Heat Risk")

fig = px.box(
    df,
    x="Heat Risk",
    y="Predicted Temperature",
    color="Heat Risk",
    template="plotly_white",
    title="Predicted Temperature by Heat Risk"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

# ============================================
# Interactive Table
# ============================================

st.subheader("Heat Risk Dataset")

risk_filter = st.multiselect(

    "Select Risk Level",

    options=df["Heat Risk"].unique(),

    default=df["Heat Risk"].unique()

)

filtered = df[
    df["Heat Risk"].isin(risk_filter)
]

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

download_csv(
    filtered,
    "heat_risk_filtered.csv"
)

st.divider()

# ============================================
# Summary
# ============================================

st.subheader("Heat Risk Summary")

st.success(f"""
Total Zones : {len(df)}

Average Predicted Temperature : {avg_temp:.2f} °C

Average Heat Score : {avg_score:.2f}

Extreme Heat Zones : {extreme}

High Heat Zones : {high}

Moderate Heat Zones : {moderate}

Low Heat Zones : {low}
""")

footer()