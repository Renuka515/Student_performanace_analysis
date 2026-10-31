"""Shared data loading, cleaning and calculation functions."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "data" / "student_performance.csv"
SUBJECTS = ["Python", "SQL", "Power BI", "AI"]

def load_data():
    """Load the project CSV dataset."""
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")
    return pd.read_csv(DATA_FILE)

def get_subject_columns(data):
    return [column for column in SUBJECTS if column in data.columns]

def prepare_data(raw):
    """Clean missing values and calculate student performance fields."""
    data = raw.copy()
    numeric = get_subject_columns(data) + (["Attendance"] if "Attendance" in data.columns else [])
    missing_before = int(data[numeric].isna().sum().sum())
    duplicates_before = int(data.duplicated().sum())

    for column in numeric:
        data[column] = pd.to_numeric(data[column], errors="coerce")
        median = data[column].median()
        data[column] = data[column].fillna(0 if pd.isna(median) else median)

    # Keep zero values as recorded scores; report them for manual review.
    zero_count = int((data[numeric] == 0).sum().sum())
    data["Total Marks"] = data[get_subject_columns(data)].sum(axis=1)
    data["Average"] = data[get_subject_columns(data)].mean(axis=1).round(2)
    data["Grade"] = data["Average"].apply(assign_grade)
    data["Rank"] = data["Average"].rank(method="min", ascending=False).astype(int)
    data = data.sort_values(["Rank", "Student"]).reset_index(drop=True)

    cleaning = {
        "Missing numeric values detected and filled": missing_before,
        "Duplicate rows detected": duplicates_before,
        "Zero values retained for review": zero_count,
        "Rows after cleaning": len(data),
    }
    return data, cleaning

def assign_grade(mark):
    if mark >= 90: return "A"
    if mark >= 80: return "B"
    if mark >= 70: return "C"
    if mark >= 60: return "D"
    return "Needs Improvement"

def get_outlier_summary(data, columns=None):
    columns = columns or get_subject_columns(data)
    result = {}
    for col in columns:
        q1, q3 = data[col].quantile([0.25, 0.75])
        iqr = q3 - q1
        count = int(((data[col] < q1 - 1.5*iqr) | (data[col] > q3 + 1.5*iqr)).sum())
        result[col] = count
    return result
