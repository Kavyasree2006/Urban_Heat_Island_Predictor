import streamlit as st
import pandas as pd

from src.loader import load_dataset
from src.utils import page_title, footer, download_csv

st.set_page_config(layout="wide")

page_title(
    "📂 Data Explorer",
    "Interactive Urban Heat Dataset Explorer"
)

df = load_dataset()

# ----------------------------
# Sidebar
# ----------------------------

st.sidebar.header("🔍 Filters")

search = st.sidebar.text_input("Search City")

landcover = st.sidebar.multiselect(
    "Land Cover",
    sorted(df["Land Cover"].unique()),
    default=sorted(df["Land Cover"].unique())
)

temperature = st.sidebar.slider(
    "Temperature (°C)",
    float(df["Temperature (°C)"].min()),
    float(df["Temperature (°C)"].max()),
    (
        float(df["Temperature (°C)"].min()),
        float(df["Temperature (°C)"].max())
    )
)

humidity = st.sidebar.slider(
    "Humidity (%)",
    float(df["Humidity (%)"].min()),
    float(df["Humidity (%)"].max()),
    (
        float(df["Humidity (%)"].min()),
        float(df["Humidity (%)"].max())
    )
)

# ----------------------------
# Filter
# ----------------------------

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["City Name"].str.contains(search, case=False)
    ]

filtered = filtered[
    filtered["Land Cover"].isin(landcover)
]

filtered = filtered[
    filtered["Temperature (°C)"].between(
        temperature[0],
        temperature[1]
    )
]

filtered = filtered[
    filtered["Humidity (%)"].between(
        humidity[0],
        humidity[1]
    )
]

# ----------------------------
# KPI Cards
# ----------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("Rows", len(filtered))
c2.metric("Columns", len(filtered.columns))
c3.metric("Missing", filtered.isnull().sum().sum())
c4.metric("Duplicates", filtered.duplicated().sum())

st.divider()

# ----------------------------
# Column Selector
# ----------------------------

selected = st.multiselect(
    "Choose Columns",
    filtered.columns,
    default=list(filtered.columns)
)

filtered = filtered[selected]

# ----------------------------
# Sorting
# ----------------------------

sort = st.selectbox(
    "Sort By",
    filtered.columns
)

ascending = st.checkbox(
    "Ascending",
    True
)

filtered = filtered.sort_values(
    sort,
    ascending=ascending
)

# ----------------------------
# Dataset
# ----------------------------

st.dataframe(
    filtered,
    use_container_width=True,
    height=550
)

download_csv(
    filtered,
    "filtered_dataset.csv"
)

st.divider()

st.subheader("Statistics")

st.dataframe(
    filtered.describe(include="all"),
    use_container_width=True
)

footer()