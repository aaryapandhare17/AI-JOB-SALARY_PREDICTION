
from pathlib import Path

import joblib
import pandas as pd

# Find the project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to saved model
MODEL_PATH = BASE_DIR / "models" / "salary_prediction_model.joblib"

# Load model once
model = joblib.load(MODEL_PATH)


def predict_salary(title, description, location):

    # Create a DataFrame with the same features used in training
    job_data = pd.DataFrame([{
        "title": title,
        "description": description,
        "location": location
    }])

    # Predict salary midpoint
    prediction = model.predict(job_data)[0]

    # Convert numerical output to lakhs
    prediction_lakhs = prediction / 100000

    return round(float(prediction_lakhs), 2)
