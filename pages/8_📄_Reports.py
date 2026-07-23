import os
import streamlit as st

from src.loader import (
    load_dataset,
    load_report,
    load_heat_predictions,
    load_recommendations
)

from src.utils import page_title, footer

# =======================================================
# Page Title
# =======================================================

page_title(
    "📄 Reports & Downloads",
    "Project Summary & Export Center"
)

# =======================================================
# Load Data
# =======================================================

dataset = load_dataset()
prediction = load_heat_predictions()
recommendation = load_recommendations()
report = load_report()

# =======================================================
# Project Statistics
# =======================================================

st.subheader("Project Statistics")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Cities", len(dataset))
c2.metric("Predictions", len(prediction))
c3.metric("Recommendations", len(recommendation))
c4.metric("Dataset Columns", len(dataset.columns))

st.divider()

# =======================================================
# Executive Summary
# =======================================================

st.subheader("Executive Summary")

st.info(report)

st.divider()

# =======================================================
# Generated Files
# =======================================================

st.subheader("Download Project Files")

files = [

    "outputs/heat_risk_predictions.csv",

    "outputs/hotspot_clusters.csv",

    "outputs/urban_cooling_recommendations.csv",

    "outputs/feature_importance.csv",

    "outputs/heat_mitigation_report.txt"

]

for file in files:

    if os.path.exists(file):

        with open(file, "rb") as f:

            st.download_button(

                label=f"Download {os.path.basename(file)}",

                data=f,

                file_name=os.path.basename(file)

            )

st.divider()

# =======================================================
# Final Project Summary
# =======================================================

st.subheader("Project Deliverables")

st.success("""
✅ Urban Heat Prediction Model

✅ Heat Risk Scoring

✅ Hyperparameter Tuning

✅ KMeans Clustering

✅ DBSCAN Clustering

✅ GIS Heat Maps

✅ Urban Cooling Recommendation Engine

✅ Interactive Streamlit Dashboard

✅ Machine Learning Model Export

✅ Smart City Analytics Report
""")

st.divider()

st.subheader("Technologies Used")

st.code("""
Python
Pandas
NumPy
Scikit-Learn
XGBoost
Plotly
Folium
Streamlit
Joblib
""")

footer()