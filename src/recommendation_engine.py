import pandas as pd


def generate_recommendation(row):
    """
    Generate cooling recommendations based on
    predicted temperature and heat risk.
    """

    risk = row["Heat Risk"]

    temp = row["Predicted Temperature"]

    green = row["Urban Greenness Ratio (%)"]

    energy = row["Energy Consumption (kWh)"]

    recommendations = []

    # -----------------------------
    # Tree Plantation
    # -----------------------------

    if green < 30:
        recommendations.append(
            "🌳 High Priority Tree Plantation"
        )

    elif green < 50:
        recommendations.append(
            "🌿 Moderate Tree Plantation"
        )

    else:
        recommendations.append(
            "✅ Existing Green Cover Sufficient"
        )

    # -----------------------------
    # Green Roof
    # -----------------------------

    if risk in ["High", "Extreme"]:

        recommendations.append(
            "🏢 Install Green Roofs"
        )

    # -----------------------------
    # Cool Pavements
    # -----------------------------

    if temp > 30:

        recommendations.append(
            "🛣 Use Reflective Pavements"
        )

    # -----------------------------
    # Water Bodies
    # -----------------------------

    if temp > 35:

        recommendations.append(
            "💧 Add Urban Water Features"
        )

    # -----------------------------
    # Energy Reduction
    # -----------------------------

    if energy > 3000:

        recommendations.append(
            "⚡ Reduce Energy Consumption"
        )

    return "\n".join(recommendations)


def create_report(df):

    df["Recommendations"] = df.apply(
        generate_recommendation,
        axis=1
    )

    return df