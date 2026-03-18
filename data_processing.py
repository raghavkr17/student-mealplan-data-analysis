"""CSE 163 Meal Plan Analysis data processing functions.

Author: Raghav Krishna

This module handles loading and cleaning the USDA Food Expenditure
dataset and the Student Food Spending Survey dataset.
"""

from __future__ import annotations

import os
from typing import Optional, Tuple

import pandas as pd

USDA_FILE = "food_expenditure.csv"
SURVEY_FILE = "student_food_survey.csv"


def _resolve_path(path: str) -> str:
    """Resolve a file path from the current or parent directory."""
    if os.path.exists(path):
        return path

    parent_path = os.path.join(os.path.dirname(__file__), "..", path)
    parent_path = os.path.abspath(parent_path)
    if os.path.exists(parent_path):
        return parent_path

    return path


def load_data(
    usda_path: str = USDA_FILE,
    survey_path: str = SURVEY_FILE,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Load USDA and survey datasets from CSV files."""
    usda = pd.read_csv(_resolve_path(usda_path))
    survey = pd.read_csv(_resolve_path(survey_path))
    return usda, survey


def _find_col(df: pd.DataFrame, contains: str) -> Optional[str]:
    """Return the first column whose name contains the given substring."""
    contains_lower = contains.lower()
    for col in df.columns:
        if contains_lower in col.lower():
            return col
    return None


def clean_usda(df: pd.DataFrame) -> pd.DataFrame:
    """Clean USDA data and standardize key columns.

    Creates these columns:
    - Year
    - Month
    - Date
    - Food Away From Home
    - Food At Home
    - Schools and Colleges share (if available)
    """
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    year_col = _find_col(df, "year")
    if year_col is None:
        raise KeyError("USDA dataset is missing a Year column.")

    df["Year"] = pd.to_numeric(df[year_col], errors="coerce").astype("Int64")
    df = df.dropna(subset=["Year"]).copy()
    df["Year"] = df["Year"].astype(int)

    month_col = _find_col(df, "month")
    if month_col is None:
        df["Month"] = 1
    else:
        df["Month"] = pd.to_numeric(df[month_col], errors="coerce").fillna(1)
        df["Month"] = df["Month"].astype(int)

    df["Date"] = pd.to_datetime(
        df["Year"].astype(str) + "-" + df["Month"].astype(str),
        errors="coerce",
    )

    fafh_col = _find_col(df, "food-away-from-home")
    if fafh_col is None:
        fafh_col = _find_col(df, "away from home")

    fah_col = _find_col(df, "food-at-home")
    if fah_col is None:
        fah_col = _find_col(df, "at home")

    if fafh_col is None or fah_col is None:
        raise KeyError(
            "USDA dataset is missing food-at-home or "
            "food-away-from-home columns."
        )

    df["Food Away From Home"] = (
        df[fafh_col].astype(str).str.replace(",", "", regex=False)
    )
    df["Food Away From Home"] = pd.to_numeric(
        df["Food Away From Home"], errors="coerce"
    )

    df["Food At Home"] = (
        df[fah_col].astype(str).str.replace(",", "", regex=False)
    )
    df["Food At Home"] = pd.to_numeric(df["Food At Home"], errors="coerce")

    share_col = _find_col(df, "schools")
    if share_col is None:
        share_col = _find_col(df, "colleges")

    if share_col is not None:
        df["Schools and Colleges share"] = pd.to_numeric(
            df[share_col].astype(str).str.replace(",", "", regex=False),
            errors="coerce",
        )

    return df


def clean_survey(df: pd.DataFrame) -> pd.DataFrame:
    """Clean survey data and standardize key columns."""
    df = df.copy()
    df.columns = [col.strip() for col in df.columns]

    if "Year in School" not in df.columns and "Grade" in df.columns:
        df["Year in School"] = df["Grade"]

    money_col = None

    # First check common exact names
    candidates = [
        "Weekly Food Spending",
        "Weekly Money",
        "weekly_money",
        "weekly spend",
        "Money",
    ]
    for candidate in candidates:
        if candidate in df.columns:
            money_col = candidate
            break

    # If no exact match, try a more flexible search
    if money_col is None:
        for col in df.columns:
            col_low = col.lower().strip()
            if "money" in col_low or "spend" in col_low:
                money_col = col
                break

    if money_col is not None:
        df["Weekly Food Spending"] = df[money_col]

    return df
