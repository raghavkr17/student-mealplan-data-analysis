# Meal Plan Spending Analysis

This project analyzes how college students spend money on food and compares student behavior with long-term national food expenditure trends.

Meal plans are a major financial component of college life, but many students still spend additional money on outside food. This project explores student spending patterns and connects them to broader trends in food consumption.

---

## Project Overview

This project investigates:

- How much students spend weekly on food
- Whether food spending patterns differ by year in school
- How student food spending compares to national trends in food purchases

The analysis uses real datasets and applies Python-based data cleaning, exploratory data analysis, and visualization.

---

## Data Sources

This project uses three main sources:

1. **USDA Food Expenditure Series**
   - National dataset tracking trends in food-at-home vs food-away-from-home spending.

2. **Kaggle Student Food Spending Survey**
   - Survey dataset containing weekly student food spending and dining habits.

3. **EducationData.org College Spending Benchmarks**
   - Used as reference statistics for average college student food spending.

CSV files for the USDA dataset and student survey are included in this repository.

---

## Requirements

This project uses Python.

Required libraries:

- pandas  
- matplotlib  

Install them using:
pip install pandas matplotlib

---

## How to Run the Project

1. Clone or download this repository.

2. Ensure the CSV data files are located in the same directory as the Python scripts.

3. Run the main analysis script:
python mealplan_analysis.py

4. The program will:

- Load and clean both datasets
- Print summary statistics and missing data information
- Generate visualizations
- Save figures into a folder named `figures`

---

## Testing

Testing is included in:
test_mealplan_analysis.py

This file validates key data processing functions to ensure the analysis results are correct and reproducible.

---

## Key Findings

- Student food spending varies significantly across individuals.
- Upper-year students show slightly more variation in outside food spending.
- National trends show increasing spending on food-away-from-home.
- Student behavior may reflect broader societal shifts toward convenience and prepared food.

---

## Future Work

Possible extensions include:

- Using real campus dining transaction data
- Studying the impact of housing status or income level
- Analyzing how meal plan structure influences spending behavior

---

## Author

Raghav Krishna  
CSE 163 Final Project
