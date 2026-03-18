"""CSE 163 tests for meal plan analysis.

Author: Raghav Krishna

These tests check important USDA cleaning behavior:
- numeric conversion with commas
- Date creation
- default month handling
- nonnegative cleaned values in test data
"""

from __future__ import annotations

import pandas as pd

from data_processing import clean_survey, clean_usda


def test_numeric_conversion_handles_commas() -> None:
    """Test that comma-formatted USDA values become numeric."""
    df = pd.DataFrame(
        {
            "Year": [2020, 2020],
            "Month": [1, 2],
            "Total food-away-from-home expenditures": ["10,000", "20,000"],
            "Total food-at-home expenditures": ["5,000", "15,000"],
        }
    )

    cleaned = clean_usda(df)

    assert cleaned["Food Away From Home"].dtype != object
    assert cleaned["Food At Home"].dtype != object
    assert cleaned["Food Away From Home"].iloc[0] == 10000
    assert cleaned["Food At Home"].iloc[1] == 15000


def test_date_creation() -> None:
    """Test that a valid Date column is created."""
    df = pd.DataFrame(
        {
            "Year": [2020],
            "Month": [1],
            "Total food-away-from-home expenditures": ["10"],
            "Total food-at-home expenditures": ["5"],
        }
    )

    cleaned = clean_usda(df)

    assert "Date" in cleaned.columns
    assert pd.notnull(cleaned["Date"]).all()


def test_default_month_creation() -> None:
    """Test that Month defaults to 1 when missing."""
    df = pd.DataFrame(
        {
            "Year": [2020],
            "Total food-away-from-home expenditures": ["10"],
            "Total food-at-home expenditures": ["5"],
        }
    )

    cleaned = clean_usda(df)

    assert "Month" in cleaned.columns
    assert cleaned["Month"].iloc[0] == 1


def test_no_negative_values_in_cleaned_test_data() -> None:
    """Test that cleaned numeric values stay nonnegative in test input."""
    df = pd.DataFrame(
        {
            "Year": [2020],
            "Month": [1],
            "Total food-away-from-home expenditures": ["10"],
            "Total food-at-home expenditures": ["5"],
        }
    )

    cleaned = clean_usda(df)

    assert (cleaned["Food Away From Home"] >= 0).all()
    assert (cleaned["Food At Home"] >= 0).all()


def test_clean_survey_creates_year_and_spending_columns() -> None:
    """Test that survey cleaning standardizes key columns."""
    df = pd.DataFrame(
        {
            "Grade": ["10th", "11th"],
            "Money": ["25", "30"],
        }
    )

    cleaned = clean_survey(df)

    assert "Year in School" in cleaned.columns
    assert "Weekly Food Spending" in cleaned.columns
    assert cleaned["Year in School"].iloc[0] == "10th"
    assert cleaned["Weekly Food Spending"].iloc[1] == "30"


if __name__ == "__main__":
    test_numeric_conversion_handles_commas()
    test_date_creation()
    test_default_month_creation()
    test_no_negative_values_in_cleaned_test_data()
    test_clean_survey_creates_year_and_spending_columns()
    print("All tests passed.")
