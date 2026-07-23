import os
import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit.components.v1 as components

from src.loader import load_hotspots
from src.utils import page_title, footer, download_csv

from src.charts import (
    hotspot_map,
    kmeans_scatter,
    dbscan_scatter
)

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Urban Heat Hotspots",
    page_icon="🗺️",
    layout="wide"
)

# ==========================================================
# TITLE
# ==========================================================

page_title(
    "🗺️ Urban Heat Hotspots",
    "Spatial Analysis • GIS • Clustering • Heat Mapping"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_hotspots()

if df.empty:
    st.error("hotspot_clusters.csv not found.")
    st.stop()

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("🔍 Filters")

risk = st.sidebar.multiselect(
    "Heat Risk",
    sorted(df["Heat Risk"].unique()),
    default=sorted(df["Heat Risk"].unique())
)

cluster = st.sidebar.multiselect(
    "KMeans Cluster",
    sorted(df["KMeans Cluster"].unique()),
    default=sorted(df["KMeans Cluster"].unique())
)

df = df[
    df["Heat Risk"].isin(risk)
]

df = df[
    df["KMeans Cluster"].isin(cluster)
]

# ==========================================================
# KPI CARDS
# ==========================================================

total = len(df)

avg_temp = df["Predicted Temperature"].mean()

avg_score = df["Heat Risk Score"].mean()

kmeans = df["KMeans Cluster"].nunique()

dbscan = df["DBSCAN Cluster"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("📍 Locations", total)

c2.metric(
    "🌡 Avg Temp",
    f"{avg_temp:.2f}°C"
)

c3.metric(
    "🔥 Avg Score",
    f"{avg_score:.1f}"
)

c4.metric(
    "🎯 KMeans",
    kmeans
)

c5.metric(
    "🛰 DBSCAN",
    dbscan
)

st.divider()

# ==========================================================
# HEAT RISK DISTRIBUTION
# ==========================================================

left, right = st.columns(2)

with left:

    fig = px.histogram(
        df,
        x="Heat Risk",
        color="Heat Risk",
        template="plotly_white",
        title="Heat Risk Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    fig = px.pie(
        df,
        names="Heat Risk",
        hole=0.45,
        title="Heat Risk Percentage"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# ==========================================================
# INTERACTIVE MAP
# ==========================================================

st.subheader("🌍 Interactive Urban Heat Map")

st.plotly_chart(
    hotspot_map(df),
    use_container_width=True
)

st.divider()

# ==========================================================
# CLUSTER VISUALIZATION
# ==========================================================

left, right = st.columns(2)

with left:

    st.subheader("KMeans Clusters")

    st.plotly_chart(
        kmeans_scatter(df),
        use_container_width=True
    )

with right:

    st.subheader("DBSCAN Clusters")

    st.plotly_chart(
        dbscan_scatter(df),
        use_container_width=True
    )

st.divider()

# ==========================================================
# CLUSTER STATISTICS
# ==========================================================

st.subheader("📊 Cluster Statistics")

summary = (

    df.groupby("KMeans Cluster")

    .agg({

        "Predicted Temperature":["mean","max"],

        "Heat Risk Score":"mean",

        "City Name":"count"

    })

)

summary.columns = [

    "Average Temperature",

    "Maximum Temperature",

    "Average Heat Score",

    "Locations"

]

st.dataframe(
    summary,
    use_container_width=True
)

st.divider()

# ==========================================================
# FOLIUM MAP
# ==========================================================

st.subheader("🗺 Folium Heat Map")

folium_file = "outputs/urban_heatmap.html"

if os.path.exists(folium_file):

    with open(folium_file, "r", encoding="utf-8") as f:

        components.html(
            f.read(),
            height=650,
            scrolling=True
        )

else:

    st.warning("urban_heatmap.html not found.")

st.divider()

# ==========================================================
# PLOTLY HTML MAP
# ==========================================================

st.subheader("🌐 Interactive Plotly HTML Map")

plotly_file = "outputs/plotly_heatmap.html"

if os.path.exists(plotly_file):

    with open(plotly_file, "r", encoding="utf-8") as f:

        components.html(
            f.read(),
            height=700,
            scrolling=True
        )

else:

    st.warning("plotly_heatmap.html not found.")

st.divider()

# ==========================================================
# FILTERED DATASET
# ==========================================================

st.subheader("📋 Explore Hotspot Dataset")

selected = st.multiselect(

    "Select Cluster",

    sorted(df["KMeans Cluster"].unique()),

    default=sorted(df["KMeans Cluster"].unique())

)

filtered = df[
    df["KMeans Cluster"].isin(selected)
]

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

download_csv(
    filtered,
    "filtered_hotspots.csv"
)

st.divider()

# ==========================================================
# SUMMARY
# ==========================================================

st.success(f"""

### Urban Heat Hotspot Summary

📍 Total Locations : **{len(filtered)}**

🌡 Average Temperature : **{filtered['Predicted Temperature'].mean():.2f} °C**

🔥 Average Heat Score : **{filtered['Heat Risk Score'].mean():.2f}**

🎯 KMeans Clusters : **{filtered['KMeans Cluster'].nunique()}**

🛰 DBSCAN Clusters : **{filtered['DBSCAN Cluster'].nunique()}**

""")

footer()