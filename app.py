import streamlit as st
import pandas as pd
import os
from src.loader import load_dataset

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="Urban Heat Island Predictor",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Load Custom CSS
# ==============================
css_path = "assets/style.css"
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ==============================
# Load Dataset
# ==============================
df = load_dataset()

# ==============================
# Sidebar
# ==============================
with st.sidebar:
    st.image(
        "https://cdn-icons-png.flaticon.com/512/4144/4144740.png",
        width=100,
    )

    st.title("Urban Heat")

    st.markdown("---")

    st.success("✔ Dashboard Ready")

    st.info(
        """
This project predicts Urban Heat Island (UHI)
intensity using Machine Learning and
Geospatial Analytics.
"""
    )

    st.markdown("---")

    st.subheader("Project Modules")

    st.write("📊 Dashboard")
    st.write("📂 Data Explorer")
    st.write("📈 EDA")
    st.write("🤖 ML Model")
    st.write("🔥 Heat Risk")
    st.write("🗺 Hotspots")
    st.write("🌳 Recommendations")
    st.write("📄 Reports")

    st.markdown("---")

    st.caption("Developed using Streamlit")

# ==============================
# Header
# ==============================
st.markdown(
    """
<h1 style='text-align:center;color:#2E8B57'>
🌍 Urban Heat Island Predictor
</h1>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<p style='text-align:center;font-size:18px'>
Machine Learning • Geospatial Analytics • Smart City Sustainability
</p>
""",
    unsafe_allow_html=True,
)

st.markdown("---")

# ==============================
# KPI Cards
# ==============================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Cities",
        len(df)
    )

with col2:
    st.metric(
        "Average Temperature",
        f"{df['Temperature (°C)'].mean():.2f} °C"
    )

with col3:
    st.metric(
        "Maximum Temperature",
        f"{df['Temperature (°C)'].max():.2f} °C"
    )

with col4:
    st.metric(
        "Average Humidity",
        f"{df['Humidity (%)'].mean():.2f}%"
    )

st.markdown("---")

# ==============================
# Project Overview
# ==============================
st.subheader("📌 Project Overview")

st.write(
"""
Urban Heat Islands (UHIs) occur when urban areas
experience significantly higher temperatures than
their surrounding rural regions due to:

- Dense buildings
- Concrete surfaces
- Reduced vegetation
- High energy consumption
- Air pollution

This project predicts heat intensity using Machine
Learning and provides urban cooling recommendations.
"""
)

# ==============================
# Dataset Preview
# ==============================
st.subheader("📂 Dataset Preview")

st.dataframe(df.head(10), use_container_width=True)

# ==============================
# Dataset Summary
# ==============================
st.subheader("📈 Dataset Summary")

left, right = st.columns(2)

with left:
    st.write("Shape")
    st.success(f"{df.shape[0]} rows × {df.shape[1]} columns")

    st.write("Missing Values")
    st.success(df.isnull().sum().sum())

with right:
    st.write("Numerical Features")
    st.success(len(df.select_dtypes(include="number").columns))

    st.write("Categorical Features")
    st.success(len(df.select_dtypes(include="object").columns))

# ==============================
# Feature List
# ==============================
st.subheader("📋 Available Features")

features = list(df.columns)

st.write(features)

# ==============================
# Workflow
# ==============================
st.subheader("⚙ Machine Learning Workflow")

workflow = """
Dataset

⬇

Data Cleaning

⬇

EDA

⬇

Feature Engineering

⬇

Random Forest

⬇

Prediction

⬇

Heat Risk

⬇

Hotspot Detection

⬇

Recommendation Engine

⬇

Dashboard
"""

st.code(workflow)

# ==============================
# Technologies
# ==============================
st.subheader("🛠 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.info(
"""
Python

Pandas

NumPy

Scikit-Learn
"""
    )

with tech2:
    st.info(
"""
Plotly

Matplotlib

Folium

Streamlit
"""
    )

with tech3:
    st.info(
"""
Random Forest

Gradient Boosting

KMeans

DBSCAN
"""
    )

# ==============================
# Footer
# ==============================
st.markdown("---")

st.markdown(
"""
<div style='text-align:center'>
<h4>Urban Heat Island Prediction System</h4>

Machine Learning | GIS | Environmental Analytics

Developed using Streamlit
</div>
""",
unsafe_allow_html=True
)