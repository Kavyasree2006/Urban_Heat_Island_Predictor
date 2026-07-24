"""
loader.py

Handles loading datasets, trained models,
and generated output files for the dashboard.
"""

import os
import pandas as pd
import joblib
import streamlit as st

def load_metrics():

    import os
    import pandas as pd

    path = "outputs/model_metrics.csv"

    if os.path.exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()
# ============================================================
# Folder Paths
# ============================================================

DATASET_PATH = "dataset/urban_heat_island_dataset.csv"

MODEL_PATH = "models/best_random_forest.pkl"

OUTPUT_FOLDER = "outputs"

# ============================================================
# Dataset Loader
# ============================================================

@st.cache_data
def load_dataset():
    """
    Load the original dataset.
    """

    if not os.path.exists(DATASET_PATH):
        st.error(f"Dataset not found:\n{DATASET_PATH}")
        st.stop()

    df = pd.read_csv(DATASET_PATH)

    return df


# ============================================================
# Model Loader
# ============================================================

@st.cache_resource
def load_model():
    """
    Load trained Random Forest model.
    """

    if not os.path.exists(MODEL_PATH):
        st.error(f"Model not found:\n{MODEL_PATH}")
        st.stop()

    model = joblib.load(MODEL_PATH)

    return model


# ============================================================
# Heat Risk Predictions
# ============================================================

@st.cache_data
def load_hotspots():

    hotspot_file = os.path.join(
        OUTPUT_FOLDER,
        "hotspot_clusters.csv"
    )

    prediction_file = os.path.join(
        OUTPUT_FOLDER,
        "heat_risk_predictions.csv"
    )

    if not os.path.exists(hotspot_file):
        return pd.DataFrame()

    hotspot_df = pd.read_csv(hotspot_file)

    if os.path.exists(prediction_file):

        prediction_df = pd.read_csv(prediction_file)

        # Add Heat Risk if missing
        if (
            "Heat Risk" not in hotspot_df.columns
            and "Heat Risk" in prediction_df.columns
        ):
            hotspot_df["Heat Risk"] = prediction_df["Heat Risk"]

        # Add Heat Risk Score if missing
        if (
            "Heat Risk Score" not in hotspot_df.columns
            and "Heat Risk Score" in prediction_df.columns
        ):
            hotspot_df["Heat Risk Score"] = prediction_df["Heat Risk Score"]

    return hotspot_df

# ============================================================
# Cooling Recommendations
# ============================================================

@st.cache_data
def load_recommendations():

    file = os.path.join(
        OUTPUT_FOLDER,
        "urban_cooling_recommendations.csv"
    )

    if os.path.exists(file):
        return pd.read_csv(file)

    return pd.DataFrame()


# ============================================================
# Hotspot Clusters
# ============================================================

@st.cache_data
def load_hotspots():

    file = os.path.join(
        OUTPUT_FOLDER,
        "hotspot_clusters.csv"
    )

    if os.path.exists(file):
        return pd.read_csv(file)

    return pd.DataFrame()


# ============================================================
# Feature Importance
# ============================================================

@st.cache_data
def load_feature_importance():

    file = os.path.join(
        OUTPUT_FOLDER,
        "feature_importance.csv"
    )

    if os.path.exists(file):
        return pd.read_csv(file)

    return pd.DataFrame()


# ============================================================
# Heat Mitigation Report
# ============================================================

@st.cache_data
def load_report():

    file = os.path.join(
        OUTPUT_FOLDER,
        "heat_mitigation_report.txt"
    )

    if os.path.exists(file):

        with open(file, "r", encoding="utf-8") as f:
            return f.read()

    return "Report not found."


# ============================================================
# Utility
# ============================================================

def file_exists(path):
    """
    Returns True if file exists.
    """

    return os.path.exists(path)
