
import sys
from pathlib import Path

import streamlit as st


import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from src.analytics import (
    load_jobs,
    get_dashboard_stats,
    get_role_salary,
    get_top_locations
)

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


        
# -------------------------------
# JOB MARKET ANALYTICS DASHBOARD
# -------------------------------

st.divider()
st.header("📊 Job Market Intelligence Dashboard")

@st.cache_data
def get_jobs_data():
    return load_jobs()

df = get_jobs_data()

# Interactive role filter
roles = ["All Roles"] + sorted(df["search_role"].dropna().unique().tolist())

selected_role = st.selectbox(
    "Select a Job Role",
    roles,
    key="analytics_role"
)


# Filter jobs by selected role
if selected_role != "All Roles":
    filtered_df = df[df["search_role"] == selected_role].copy()
else:
    filtered_df = df.copy()

# Location filter based on available jobs
locations = ["All Locations"] + sorted(
    filtered_df["location"].dropna().unique().tolist()
)

selected_location = st.selectbox(
    "Select a Location",
    locations,
    key="analytics_location"
)

# Apply location filter
if selected_location != "All Locations":
    filtered_df = filtered_df[
        filtered_df["location"] == selected_location
    ]

# Handle empty results
if filtered_df.empty:
    st.warning("No jobs found for the selected filters.")
    st.stop()


# Dashboard statistics
stats = get_dashboard_stats(filtered_df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Jobs", stats["total_jobs"])
col2.metric("Average Salary", f"₹{stats['average_salary']} LPA")
col3.metric("Median Salary", f"₹{stats['median_salary']} LPA")
col4.metric("Locations", stats["total_locations"])

st.divider()


# Salary distribution histogram
st.subheader("Salary Distribution")

import altair as alt

salary_chart = (
    alt.Chart(filtered_df)
    .mark_bar(color="#16A085")
    .encode(
        x=alt.X(
            "salary_lpa:Q",
            bin=alt.Bin(maxbins=15),
            title="Salary (LPA)"
        ),
        y=alt.Y(
            "count():Q",
            title="Number of Jobs"
        ),
        tooltip=[
            alt.Tooltip("count():Q", title="Number of Jobs")
        ]
    )
    .properties(height=350)
)

st.altair_chart(salary_chart, use_container_width=True)


# Average salary by role
st.subheader("Average Salary by Job Role")

role_salary = get_role_salary(filtered_df)

st.bar_chart(
    role_salary.set_index("search_role")["mean"]
)

# Top job locations
st.subheader("Top Job Locations")

top_locations = get_top_locations(filtered_df)

st.bar_chart(
    top_locations.set_index("Location")["Jobs"]
)

st.caption(
    "These insights are based on collected Adzuna job listings "
    "and do not represent the entire Indian job market. "
    "Salary values are provisional annual INR estimates."
)

