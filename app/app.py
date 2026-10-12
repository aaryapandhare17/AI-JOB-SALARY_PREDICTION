
import sys
from pathlib import Path

import streamlit as st

# Allow imports from the project root
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.predict import predict_salary

st.set_page_config(
    page_title="AI Job & Salary Intelligence",
    page_icon="💼",
    layout="centered"
)

st.title("💼 AI Job & Salary Intelligence")
st.write("Predict an experimental salary midpoint using Machine Learning.")

st.subheader("Enter Job Details")

title = st.text_input(
    "Job Title",
    placeholder="e.g. Machine Learning Engineer"
)

description = st.text_area(
    "Job Description",
    placeholder="Enter skills, responsibilities and experience...",
    height=150
)

location = st.selectbox(
    "Job Location",
    [
        "Bangalore, Karnataka",
        "Pune, Maharashtra",
        "Hyderabad, Telangana",
        "Mumbai, Maharashtra",
        "Chennai, Tamil Nadu",
        "Delhi",
        "India"
    ]
)

if st.button("Predict Salary", type="primary"):

    if not title.strip() or not description.strip():
        st.warning("Please enter both job title and description.")

    else:
        with st.spinner("Predicting salary..."):
            prediction = predict_salary(
                title.strip(),
                description.strip(),
                location
            )

        st.success("Prediction completed!")

        st.metric(
            label="Estimated Salary Midpoint",
            value=f"{prediction:.2f} lakh"
        )

        st.caption(
            "Experimental prediction based on a limited job-listing "
            "dataset. Salary units and model accuracy require further "
            "validation. Not a guaranteed or verified annual salary."
        )
