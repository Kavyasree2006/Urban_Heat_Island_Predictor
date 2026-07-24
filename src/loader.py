"""
loader.py

Handles loading datasets, trained models,
and generated output files for the dashboard.
"""

import os
import joblib
import pandas as pd
import streamlit as st

# ============================================================
# Folder Paths
# ============================================================

DATASET_PATH = "dataset/urban_heat_island_dataset.csv"
MODEL_PATH = "models/best_random_forest.pkl"
OUTPUT_FOLDER = "outputs"

# ============================================================
# Utility
# ============================================================

def file_exists(path):
    return os.path.exists(path)


# ============================================================
# Dataset Loader
# ============================================================

@st.cache_data
def load_dataset():

    if not file_exists(DATASET_PATH):
        st.error(f"Dataset not found:\n{DATASET_PATH}")
        return pd.DataFrame()

    return pd.read_csv(DATASET_PATH)


# ============================================================
# Model Loader
# ============================================================

@st.cache_resource
def load_model():

    if not file_exists(MODEL_PATH):
        st.error(f"Model not found:\n{MODEL_PATH}")
        return None

    return joblib.load(MODEL_PATH)


# ============================================================
# Model Metrics
# ============================================================

@st.cache_data
def load_metrics():

    path = os.path.join(
        OUTPUT_FOLDER,
        "model_metrics.csv"
    )

    if file_exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


# ============================================================
# Heat Risk Predictions
# ============================================================

@st.cache_data
def load_heat_predictions():

    path = os.path.join(
        OUTPUT_FOLDER,
        "heat_risk_predictions.csv"
    )

    if file_exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


# ============================================================
# Cooling Recommendations
# ============================================================

@st.cache_data
def load_recommendations():

    path = os.path.join(
        OUTPUT_FOLDER,
        "urban_cooling_recommendations.csv"
    )

    if file_exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


# ============================================================
# Feature Importance
# ============================================================

@st.cache_data
def load_feature_importance():

    path = os.path.join(
        OUTPUT_FOLDER,
        "feature_importance.csv"
    )

    if file_exists(path):
        return pd.read_csv(path)

    return pd.DataFrame()


# ============================================================
# Hotspot Loader (Fixed)
# ============================================================

@st.cache_data
def load_hotspots():

    hotspot_path = os.path.join(
        OUTPUT_FOLDER,
        "hotspot_clusters.csv"
    )

    prediction_path = os.path.join(
        OUTPUT_FOLDER,
        "heat_risk_predictions.csv"
    )

    if not file_exists(hotspot_path):
        st.warning("hotspot_clusters.csv not found.")
        return pd.DataFrame()

    hotspot = pd.read_csv(hotspot_path)

    # Merge with prediction file if available
    if file_exists(prediction_path):

        prediction = pd.read_csv(prediction_path)

        merge_columns = [
            "City Name",
            "Predicted Temperature",
            "Heat Risk",
            "Heat Risk Score",
            "Urban Greenness Ratio (%)"
        ]

        available_columns = [
            col for col in merge_columns
            if col in prediction.columns
        ]

        if "City Name" in available_columns:

            hotspot = hotspot.merge(
                prediction[available_columns],
                on="City Name",
                how="left",
                suffixes=("", "_pred")
            )

    # Remove duplicate columns after merge
    for column in list(hotspot.columns):

        if column.endswith("_pred"):

            original = column.replace("_pred", "")

            if original not in hotspot.columns:
                hotspot.rename(
                    columns={column: original},
                    inplace=True
                )
            else:
                hotspot.drop(
                    columns=column,
                    inplace=True
                )

    # Ensure required columns exist
    required_columns = {
        "Heat Risk": "Unknown",
        "Heat Risk Score": 0,
        "Predicted Temperature": 0,
        "Urban Greenness Ratio (%)": 0
    }

    for column, default in required_columns.items():

        if column not in hotspot.columns:
            hotspot[column] = default

    return hotspot


# ============================================================
# Report Loader
# ============================================================

@st.cache_data
def load_report():

    path = os.path.join(
        OUTPUT_FOLDER,
        "heat_mitigation_report.txt"
    )

    if file_exists(path):

        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    return "Heat mitigation report not found."


# ============================================================
# Dashboard Status
# ============================================================

@st.cache_data
def dashboard_status():

    return {
        "Dataset": file_exists(DATASET_PATH),
        "Model": file_exists(MODEL_PATH),
        "Predictions": file_exists(
            os.path.join(
                OUTPUT_FOLDER,
                "heat_risk_predictions.csv"
            )
        ),
        "Hotspots": file_exists(
            os.path.join(
                OUTPUT_FOLDER,
                "hotspot_clusters.csv"
            )
        ),
        "Recommendations": file_exists(
            os.path.join(
                OUTPUT_FOLDER,
                "urban_cooling_recommendations.csv"
            )
        ),
        "Feature Importance": file_exists(
            os.path.join(
                OUTPUT_FOLDER,
                "feature_importance.csv"
            )
        ),
        "Report": file_exists(
            os.path.join(
                OUTPUT_FOLDER,
                "heat_mitigation_report.txt"
            )
        ),
    }
