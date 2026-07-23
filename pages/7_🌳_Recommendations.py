import os
import streamlit as st
import plotly.express as px

from src.loader import load_recommendations
from src.utils import page_title, footer, download_csv
from src.recommendation_engine import create_report
from src.report import generate_pdf

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Urban Cooling Recommendation Engine",
    page_icon="🌳",
    layout="wide"
)

page_title(
    "🌳 Urban Cooling Recommendation Engine",
    "AI-Based Urban Heat Mitigation & Sustainability Planning"
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = load_recommendations()

if df.empty:
    st.error("urban_cooling_recommendations.csv not found.")
    st.stop()

# Generate AI recommendations
df = create_report(df)

# ==========================================================
# KPI CARDS
# ==========================================================

tree = df["Tree Plantation"].value_counts()
roof = df["Green Roof"].value_counts()

high_tree = tree.get("High Priority Tree Plantation",0)
moderate_tree = tree.get("Moderate Tree Plantation",0)
green_cover = tree.get("Existing Green Cover Sufficient",0)
roof_required = roof.get("Recommended",0)

c1,c2,c3,c4 = st.columns(4)

c1.metric("🌳 High Priority Trees",high_tree)
c2.metric("🌿 Moderate Priority",moderate_tree)
c3.metric("🏞 Existing Green Cover",green_cover)
c4.metric("🏢 Green Roof Required",roof_required)

st.divider()

# ==========================================================
# CHARTS
# ==========================================================

left,right = st.columns(2)

with left:

    st.subheader("Tree Plantation Recommendation")

    fig = px.bar(
        df["Tree Plantation"].value_counts().reset_index(),
        x="Tree Plantation",
        y="count",
        color="Tree Plantation",
        template="plotly_white"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    st.subheader("Green Roof Recommendation")

    fig = px.pie(
        df,
        names="Green Roof",
        hole=0.45
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ==========================================================
# COOLING INFRASTRUCTURE
# ==========================================================

st.subheader("Cooling Infrastructure")

infra = (
    df.groupby("Cooling Infrastructure")
    .size()
    .reset_index(name="Count")
)

fig = px.bar(
    infra,
    x="Cooling Infrastructure",
    y="Count",
    color="Cooling Infrastructure",
    template="plotly_white"
)

st.plotly_chart(fig,use_container_width=True)

st.divider()

# ==========================================================
# HEAT RISK DISTRIBUTION
# ==========================================================

left,right = st.columns(2)

with left:

    fig = px.histogram(
        df,
        x="Heat Risk",
        color="Heat Risk",
        template="plotly_white",
        title="Heat Risk Distribution"
    )

    st.plotly_chart(fig,use_container_width=True)

with right:

    fig = px.pie(
        df,
        names="Heat Risk",
        hole=0.45,
        title="Heat Risk Percentage"
    )

    st.plotly_chart(fig,use_container_width=True)

st.divider()

# ==========================================================
# FILTERS
# ==========================================================

st.subheader("Recommendation Explorer")

tree_filter = st.multiselect(
    "Tree Plantation",
    sorted(df["Tree Plantation"].unique()),
    default=sorted(df["Tree Plantation"].unique())
)

roof_filter = st.multiselect(
    "Green Roof",
    sorted(df["Green Roof"].unique()),
    default=sorted(df["Green Roof"].unique())
)

risk_filter = st.multiselect(
    "Heat Risk",
    sorted(df["Heat Risk"].unique()),
    default=sorted(df["Heat Risk"].unique())
)

filtered = df[
    (df["Tree Plantation"].isin(tree_filter))
    &
    (df["Green Roof"].isin(roof_filter))
    &
    (df["Heat Risk"].isin(risk_filter))
]

st.dataframe(
    filtered,
    use_container_width=True,
    height=500
)

st.divider()

# ==========================================================
# AI RECOMMENDATIONS
# ==========================================================

st.subheader("🤖 AI Generated Cooling Recommendations")

st.dataframe(
    filtered[
        [
            "City Name",
            "Predicted Temperature",
            "Heat Risk",
            "Recommendations"
        ]
    ],
    use_container_width=True
)

st.divider()

# ==========================================================
# SMART CITY GUIDELINES
# ==========================================================

st.subheader("🏙 Smart City Heat Mitigation Guidelines")

st.success("""
🌳 Increase tree plantation in High & Extreme heat zones.

🏢 Promote green roof implementation in commercial buildings.

🛣 Replace asphalt with cool reflective pavements.

🌊 Preserve lakes, ponds and wetlands.

🌿 Develop urban biodiversity parks.

🚲 Promote cycling and public transport.

⚡ Improve energy efficiency.

🏭 Reduce industrial heat emissions.

☀ Install solar-powered cooling infrastructure.

🌧 Increase rainwater harvesting.
""")

st.divider()

# ==========================================================
# PDF REPORT
# ==========================================================

st.subheader("📄 Report Generation")

if st.button("Generate PDF Report"):

    pdf_path = "outputs/UHI_Report.pdf"

    generate_pdf(filtered,pdf_path)

    st.success("PDF Report Generated Successfully.")

st.divider()

# ==========================================================
# DOWNLOAD CENTER
# ==========================================================

st.header("📥 Download Center")

csv = filtered.to_csv(index=False)

st.download_button(
    "📊 Download CSV",
    csv,
    file_name="urban_cooling_recommendations.csv",
    mime="text/csv"
)

txt = filtered.to_string()

st.download_button(
    "📄 Download TXT Report",
    txt,
    file_name="heat_mitigation_report.txt",
    mime="text/plain"
)

pdf_path = "outputs/UHI_Report.pdf"

if os.path.exists(pdf_path):

    with open(pdf_path,"rb") as file:

        st.download_button(
            "📘 Download PDF Report",
            file,
            file_name="Urban_Heat_Report.pdf",
            mime="application/pdf"
        )

st.divider()

# ==========================================================
# SUMMARY
# ==========================================================

st.info(f"""
### 🌍 Recommendation Summary

📍 Total Locations : **{len(filtered)}**

🌡 Average Predicted Temperature : **{filtered['Predicted Temperature'].mean():.2f} °C**

🔥 Average Heat Risk Score : **{filtered['Heat Risk Score'].mean():.2f}**

🌳 High Priority Tree Plantation : **{high_tree}**

🏢 Green Roof Recommendation : **{roof_required}**
""")

footer()