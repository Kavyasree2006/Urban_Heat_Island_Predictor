import streamlit as st
from src.loader import (
    load_dataset,
    load_heat_predictions,
    load_recommendations
)

from src.utils import (
    page_title,
    footer
)

from src.charts import (
    temperature_distribution,
    heat_risk_distribution,
    pie_chart
)

# ==============================
# Load Data
# ==============================

df = load_dataset()

heat_df = load_heat_predictions()

recommend_df = load_recommendations()

# ==============================
# Page Title
# ==============================

page_title(
    "📊 Dashboard",
    "Urban Heat Island Monitoring Dashboard"
)

# ==============================
# KPI Cards
# ==============================

total_cities = len(df)

avg_temp = df["Temperature (°C)"].mean()

max_temp = df["Temperature (°C)"].max()

avg_humidity = df["Humidity (%)"].mean()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🏙 Cities",
        total_cities
    )

with col2:

    st.metric(
        "🌡 Avg Temp",
        f"{avg_temp:.2f} °C"
    )

with col3:

    st.metric(
        "🔥 Max Temp",
        f"{max_temp:.2f} °C"
    )

with col4:

    st.metric(
        "💧 Avg Humidity",
        f"{avg_humidity:.2f}%"
    )

st.divider()

# ==============================
# Charts
# ==============================

left, right = st.columns(2)

with left:

    st.subheader("Temperature Distribution")

    fig = temperature_distribution(df)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    if not heat_df.empty:

        st.subheader("Heat Risk Distribution")

        fig = heat_risk_distribution(
            heat_df
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# ==============================
# Pie Charts
# ==============================

left, right = st.columns(2)

with left:

    st.subheader("Land Cover")

    fig = pie_chart(
        df,
        "Land Cover"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Heat Risk")

    if not heat_df.empty:

        fig = pie_chart(
            heat_df,
            "Heat Risk"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

st.divider()

# ==============================
# Dataset Preview
# ==============================

st.subheader("Dataset Preview")

st.dataframe(
    df.head(10),
    use_container_width=True
)

st.divider()

# ==============================
# Statistics
# ==============================

st.subheader("Dataset Statistics")

st.dataframe(
    df.describe(),
    use_container_width=True
)

# ==============================
# Recommendations Preview
# ==============================

if not recommend_df.empty:

    st.divider()

    st.subheader(
        "Cooling Recommendations"
    )

    st.dataframe(
        recommend_df.head(10),
        use_container_width=True
    )

footer()