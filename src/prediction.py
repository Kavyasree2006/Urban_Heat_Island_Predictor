import joblib
import pandas as pd
import os

MODEL_PATH = "models/best_model.pkl"


def load_model():
    """Load trained Random Forest model."""
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    return None


model = load_model()


def predict_temperature(features: dict):
    """
    Predict temperature from user inputs.

    Parameters
    ----------
    features : dict

    Returns
    -------
    float
    """

    if model is None:
        return None

    X = pd.DataFrame([features])

    prediction = model.predict(X)

    return float(prediction[0])


def heat_score(temp):

    score = (temp / 60) * 100

    score = max(0, min(100, score))

    return round(score, 2)


def heat_category(score):

    if score < 25:
        return "Low"

    elif score < 50:
        return "Moderate"

    elif score < 75:
        return "High"

    else:
        return "Extreme"


def recommendation(category):

    if category == "Low":

        return "Current green cover is sufficient."

    elif category == "Moderate":

        return "Increase roadside tree plantation."

    elif category == "High":

        return (
            "Implement green roofs and "
            "expand urban vegetation."
        )

    else:

        return (
            "Urgent cooling infrastructure, "
            "dense plantation and reflective materials required."
        )