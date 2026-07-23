"""
utils.py

Utility functions used throughout the
Urban Heat Island Dashboard.
"""

import streamlit as st
import pandas as pd
import base64

# ======================================================
# Page Title
# ======================================================

def page_title(title, subtitle=""):
    """
    Display a consistent page title.
    """

    st.markdown(
        f"""
        <div class='main-title'>{title}</div>
        <div class='sub-title'>{subtitle}</div>
        <hr>
        """,
        unsafe_allow_html=True,
    )


# ======================================================
# KPI Card
# ======================================================

def metric_card(title, value, delta=None):

    col = st.container()

    with col:

        st.metric(
            label=title,
            value=value,
            delta=delta
        )


# ======================================================
# Heat Risk Badge
# ======================================================

def heat_risk_badge(risk):

    colors = {

        "Low": "#2E7D32",

        "Moderate": "#F9A825",

        "High": "#EF6C00",

        "Extreme": "#C62828"

    }

    color = colors.get(risk, "#616161")

    return f"""
    <div style="
        background:{color};
        color:white;
        padding:6px;
        border-radius:8px;
        text-align:center;
        font-weight:bold;
    ">
        {risk}
    </div>
    """


# ======================================================
# Temperature Formatter
# ======================================================

def format_temperature(temp):

    return f"{temp:.2f} °C"


# ======================================================
# Percentage Formatter
# ======================================================

def format_percent(value):

    return f"{value:.2f} %"


# ======================================================
# Download CSV
# ======================================================

def download_csv(df, filename):

    csv = df.to_csv(index=False)

    st.download_button(

        label="⬇ Download CSV",

        data=csv,

        file_name=filename,

        mime="text/csv"

    )


# ======================================================
# Data Summary
# ======================================================

def dataset_summary(df):

    st.write("### Dataset Summary")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", len(df))

    c2.metric("Columns", len(df.columns))

    c3.metric(
        "Missing Values",
        int(df.isnull().sum().sum())
    )

    c4.metric(
        "Duplicates",
        int(df.duplicated().sum())
    )


# ======================================================
# Colored Success Box
# ======================================================

def success_box(message):

    st.markdown(

        f"""
        <div style="
        background:#E8F5E9;
        padding:15px;
        border-left:6px solid green;
        border-radius:8px;
        ">

        {message}

        </div>

        """,

        unsafe_allow_html=True

    )


# ======================================================
# Colored Warning Box
# ======================================================

def warning_box(message):

    st.markdown(

        f"""
        <div style="
        background:#FFF3E0;
        padding:15px;
        border-left:6px solid orange;
        border-radius:8px;
        ">

        {message}

        </div>

        """,

        unsafe_allow_html=True

    )


# ======================================================
# Colored Error Box
# ======================================================

def error_box(message):

    st.markdown(

        f"""
        <div style="
        background:#FFEBEE;
        padding:15px;
        border-left:6px solid red;
        border-radius:8px;
        ">

        {message}

        </div>

        """,

        unsafe_allow_html=True

    )


# ======================================================
# Display DataFrame
# ======================================================

def show_dataframe(df):

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True

    )


# ======================================================
# Heat Risk Color
# ======================================================

def risk_color(risk):

    colors = {

        "Low": "green",

        "Moderate": "gold",

        "High": "orange",

        "Extreme": "red"

    }

    return colors.get(risk, "gray")


# ======================================================
# Convert Image to Base64
# ======================================================

def image_to_base64(path):

    with open(path, "rb") as img:

        encoded = base64.b64encode(img.read()).decode()

    return encoded


# ======================================================
# Footer
# ======================================================

def footer():

    st.markdown("---")

    st.markdown(

        """
        <div class="footer">

        🌍 Urban Heat Island Predictor <br>

        Smart City | Machine Learning | GIS

        </div>

        """,

        unsafe_allow_html=True

    )