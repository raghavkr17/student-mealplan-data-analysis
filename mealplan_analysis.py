"""CSE 163 Meal Plan Analysis Final Project.

Author: Raghav Krishna

This script loads two datasets:
1) USDA Food Expenditure Series (CSV) for national spending trends.
2) Student Food Spending Survey (CSV) for student behavior.

It cleans data, prints EDA summaries, and saves plots.
"""

from __future__ import annotations

import os

import matplotlib.pyplot as plt
import pandas as pd

from data_processing import clean_survey, clean_usda, load_data

OUTPUT_DIR = "figures"
SAVE_PLOTS = True
SHOW_PLOTS = False


def _save_or_show(filename: str) -> None:
    """Save the current figure and optionally show it."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)

    if SAVE_PLOTS:
        plt.savefig(path, dpi=200, bbox_inches="tight")

    if SHOW_PLOTS:
        plt.show()

    plt.close()


def print_missingness(df: pd.DataFrame, name: str) -> None:
    """Print missing value counts and percentages for a dataset."""
    print(f"\n{name} missingness (count):")
    print(df.isnull().sum())
    print(f"\n{name} missingness (%):")
    print((df.isnull().mean() * 100).round(2))


def print_describe(df: pd.DataFrame, name: str) -> None:
    """Print a pandas describe summary."""
    print(f"\n{name} describe():")
    print(df.describe(include="all"))


def plot_usda_trends(df: pd.DataFrame) -> None:
    """Plot national food-away-from-home spending over time."""
    df_sorted = df.sort_values("Date")

    plt.figure()
    plt.plot(df_sorted["Date"], df_sorted["Food Away From Home"])
    plt.title("Food Away From Home Spending Over Time")
    plt.xlabel("Date")
    plt.ylabel("National Food-Away-From-Home Spending")
    _save_or_show("usda_spending_trends.png")


def plot_usda_college_component(df: pd.DataFrame) -> None:
    """Plot schools/colleges share over time if available."""
    if "Schools and Colleges share" not in df.columns:
        return

    df_sorted = df.sort_values("Date")

    plt.figure()
    plt.plot(df_sorted["Date"], df_sorted["Schools and Colleges share"])
    plt.title("Food-Away-From-Home Spending at Schools and Colleges")
    plt.xlabel("Date")
    plt.ylabel("Share of Food-Away-From-Home Spending")
    _save_or_show("usda_schools_colleges_share.png")


def plot_survey_year_counts(df: pd.DataFrame) -> None:
    """Plot number of survey responses by year in school."""
    if "Year in School" not in df.columns:
        return

    counts = df["Year in School"].value_counts()

    plt.figure()
    counts.plot(kind="bar")
    plt.title("Survey Responses by Year in School")
    plt.xlabel("Year in School")
    plt.ylabel("Number of Survey Responses")
    _save_or_show("survey_year_counts.png")


def plot_survey_money_by_year(df: pd.DataFrame) -> None:
    """Plot weekly food spending by year in school."""
    has_year = "Year in School" in df.columns
    has_spending = "Weekly Food Spending" in df.columns
    if not has_year or not has_spending:
        print("Missing required columns for survey money boxplot.")
        print("Columns found:", list(df.columns))
        return

    money = pd.to_numeric(df["Weekly Food Spending"], errors="coerce")
    temp = df[["Year in School"]].copy()
    temp["Weekly Food Spending"] = money
    temp = temp.dropna(subset=["Weekly Food Spending"])

    if temp.empty:
        print("No numeric values found in Weekly Food Spending.")
        return

    plt.figure()
    temp.boxplot(column="Weekly Food Spending", by="Year in School", rot=45)
    plt.suptitle("")
    plt.title("Weekly Food Spending by Year in School")
    plt.xlabel("Year in School")
    plt.ylabel("Weekly Food Spending ($)")
    _save_or_show("survey_money_by_year_boxplot.png")


def main() -> None:
    """Run the full EDA pipeline."""
    usda_raw, survey_raw = load_data()
    usda = clean_usda(usda_raw)
    survey = clean_survey(survey_raw)

    print_missingness(usda, "USDA")
    print_missingness(survey, "Survey")

    usda_cols = ["Food Away From Home", "Food At Home"]
    print_describe(usda[usda_cols], "USDA Spending")
    print_describe(survey, "Survey")

    plot_usda_trends(usda)
    plot_usda_college_component(usda)
    plot_survey_year_counts(survey)
    plot_survey_money_by_year(survey)

    print(f"\nSaved figures to: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
