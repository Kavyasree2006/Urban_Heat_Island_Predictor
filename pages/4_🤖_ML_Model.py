import streamlit as st
import pandas as pd
from src.loader import load_metrics
from src.charts import actual_vs_predicted_scatter
from src.charts import residual_plot
from src.loader import (
    load_model,
    load_dataset,
    load_feature_importance,
    load_heat_predictions
)

from src.charts import (
    feature_importance_chart,
    actual_vs_predicted,
    heat_gauge
)
from src.prediction import (
    predict_temperature,
    heat_score,
    heat_category,
    recommendation
)
from src.utils import page_title, footer

model = load_model()
df = load_dataset()

importance = load_feature_importance()

prediction_df = load_heat_predictions()

page_title(
    "🤖 Machine Learning Model",
    "Random Forest Heat Prediction"
)
fig = actual_vs_predicted_scatter(
    prediction_df
)
st.subheader("Residual Error Distribution")

fig = residual_plot(
    prediction_df
)

st.plotly_chart(
    fig,
    use_container_width=True
)
# =======================================
# Model Information
# =======================================

st.subheader("Model Details")

c1, c2, c3 = st.columns(3)

c1.metric("Algorithm", "Random Forest")

c2.metric("Training Samples", "400")

c3.metric("Testing Samples", "100")

st.divider()

# =======================================
# Evaluation Metrics
# =======================================

st.subheader("Evaluation")

a, b, c, d = st.columns(4)
metrics = load_metrics()

if not metrics.empty:

    rmse = metrics.loc[
        metrics["Metric"] == "RMSE",
        "Value"
    ].values[0]

    mae = metrics.loc[
        metrics["Metric"] == "MAE",
        "Value"
    ].values[0]

    mape = metrics.loc[
        metrics["Metric"] == "MAPE",
        "Value"
    ].values[0]

    r2 = metrics.loc[
        metrics["Metric"] == "R2",
        "Value"
    ].values[0]

    a.metric("RMSE", f"{rmse:.3f}")
    b.metric("MAE", f"{mae:.3f}")
    c.metric("MAPE", f"{mape:.2f}%")
    d.metric("R² Score", f"{r2:.3f}")

st.divider()

# =======================================
# Gauge
# =======================================

st.dataframe(

    importance.sort_values(
        "Importance",
        ascending=False
    ),

    use_container_width=True,

    hide_index=True

)

st.subheader("Average Heat Risk Score")

if not prediction_df.empty:

    score = prediction_df["Heat Risk Score"].mean()

    fig = heat_gauge(score)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =======================================
# Feature Importance
# =======================================

st.subheader("Feature Importance")

if not importance.empty:

    fig = feature_importance_chart(
        importance
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

# =======================================
# Actual vs Predicted
# =======================================

st.subheader("Actual vs Predicted")

if not prediction_df.empty:

    fig = actual_vs_predicted(
        prediction_df
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.divider()

st.subheader("🌍 Live AI Prediction")

left, right = st.columns(2)

with left:

    latitude = st.number_input(
        "Latitude",
        -90.0,
        90.0,
        20.0
    )

    longitude = st.number_input(
        "Longitude",
        -180.0,
        180.0,
        78.0
    )

    elevation = st.number_input(
        "Elevation (m)",
        0.0,
        5000.0,
        250.0
    )

    population = st.number_input(
        "Population Density",
        100.0,
        50000.0,
        5000.0
    )

    land_cover = st.selectbox(

        "Land Cover",

        ["Residential",
         "Commercial",
         "Industrial",
         "Green Area"]

    )

    greenness = st.slider(

        "Urban Greenness Ratio (%)",

        0,

        100,

        40

    )

with right:

    energy = st.number_input(

        "Energy Consumption (kWh)",

        100,

        10000,

        3000

    )

    aqi = st.slider(

        "Air Quality Index",

        0,

        500,

        120

    )

    humidity = st.slider(

        "Humidity (%)",

        0,

        100,

        60

    )

    wind = st.slider(

        "Wind Speed (km/h)",

        0,

        100,

        15

    )

    rainfall = st.number_input(

        "Annual Rainfall",

        0,

        4000,

        1200

    )

    gdp = st.number_input(

        "GDP per Capita",

        1000,

        100000,

        25000

    )

if st.button("🚀 Predict Heat"):

    land_cover_map = {

        "Residential": 0,

        "Commercial": 1,

        "Industrial": 2,

        "Green Area": 3

    }

    features = {

        "City Name": "Prediction",

        "Latitude": latitude,

        "Longitude": longitude,

        "Elevation (m)": elevation,

        "Land Cover": land_cover_map[land_cover],

        "Population Density (people/km²)": population,

        "Energy Consumption (kWh)": energy,

        "Air Quality Index (AQI)": aqi,

        "Urban Greenness Ratio (%)": greenness,

        "Health Impact (Mortality Rate/100k)": 0,

        "Wind Speed (km/h)": wind,

        "Humidity (%)": humidity,

        "Annual Rainfall (mm)": rainfall,

        "GDP per Capita (USD)": gdp

    }

    pred = predict_temperature(features)

    if pred is not None:

        score = heat_score(pred)

        risk = heat_category(score)

        rec = recommendation(risk)

        st.success(
            f"🌡 Predicted Temperature : {pred:.2f} °C"
        )

        st.info(
            f"🔥 Heat Risk Score : {score}"
        )

        st.warning(
            f"🚨 Heat Category : {risk}"
        )

        st.success(
            f"🌳 Recommendation : {rec}"
        )

    else:

        st.error("Model not found.")
        st.download_button(

    "📥 Download Predictions",

    prediction_df.to_csv(index=False),

    "predictions.csv",

    "text/csv"

)
footer()