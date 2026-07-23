import streamlit as st
import plotly.express as px

from src.loader import load_dataset
from src.charts import *

from src.utils import page_title, footer

st.set_page_config(layout="wide")

df = load_dataset()

page_title(
    "📈 Exploratory Data Analysis",
    "Interactive Environmental Analytics"
)

# ==========================================
# Tabs
# ==========================================

tab1, tab2, tab3, tab4 = st.tabs([

    "Overview",

    "Distribution",

    "Relationships",

    "Correlation"

])

# ==========================================
# Overview
# ==========================================

with tab1:

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Cities", len(df))

    c2.metric(
        "Avg Temp",
        f"{df['Temperature (°C)'].mean():.2f}"
    )

    c3.metric(
        "Avg Humidity",
        f"{df['Humidity (%)'].mean():.2f}"
    )

    c4.metric(
        "Avg AQI",
        f"{df['Air Quality Index (AQI)'].mean():.2f}"
    )

    st.plotly_chart(
        temperature_distribution(df),
        use_container_width=True
    )

# ==========================================
# Distribution
# ==========================================

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        fig = px.histogram(
            df,
            x="Temperature (°C)",
            color="Land Cover",
            marginal="box"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        fig = px.histogram(
            df,
            x="Humidity (%)",
            color="Land Cover"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.plotly_chart(

        box_plot(
            df,
            "Land Cover",
            "Temperature (°C)"
        ),

        use_container_width=True

    )

# ==========================================
# Relationships
# ==========================================

with tab3:

    col1, col2 = st.columns(2)

    with col1:

        fig = px.scatter(

            df,

            x="Urban Greenness Ratio (%)",

            y="Temperature (°C)",

            color="Land Cover",

            size="Population Density (people/km²)"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

    with col2:

        fig = px.scatter(

            df,

            x="Humidity (%)",

            y="Temperature (°C)",

            color="Land Cover"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

# ==========================================
# Correlation
# ==========================================

with tab4:

    st.plotly_chart(

        correlation_heatmap(df),

        use_container_width=True

    )

    st.subheader("Feature Correlation")

    numeric = df.select_dtypes(include="number")

    corr = numeric.corr()["Temperature (°C)"]

    corr = corr.sort_values(
        ascending=False
    )

    st.dataframe(
        corr,
        use_container_width=True
    )

footer()