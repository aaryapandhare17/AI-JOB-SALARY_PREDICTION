
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "processed" / "jobs_cleaned.csv"

def load_jobs():
    return pd.read_csv(DATA_PATH)

def get_dashboard_stats(df):
    return {
        "total_jobs": len(df),
        "average_salary": round(df["salary_lpa"].mean(), 2),
        "median_salary": round(df["salary_lpa"].median(), 2),
        "total_locations": df["location"].nunique()
    }

def get_role_salary(df):
    return (
        df.groupby("search_role")["salary_lpa"]
        .agg(["mean", "median", "count"])
        .round(2)
        .reset_index()
    )

def get_top_locations(df):
    return (
        df["location"]
        .value_counts()
        .head(10)
        .rename_axis("Location")
        .reset_index(name="Jobs")
    )
