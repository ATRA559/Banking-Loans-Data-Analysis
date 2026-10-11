# Banking Loans Data Analysis

## About the Project

This project analyzes banking loan data to better understand customer profiles, loan characteristics, credit risk, and lending trends.

The project includes data cleaning, exploratory data analysis, data visualization, and an interactive dashboard built with Streamlit.

## Dataset

The cleaned dataset contains 11,965 records and 21 columns. It includes customer information, loan details, credit scores, risk grades, loan statuses, and repayment information.

The loan amounts and financial figures are in Egyptian Pounds (EGP).

## Tools Used

- Python
- Pandas and NumPy
- Plotly
- Jupyter Notebook
- Streamlit

## Project Files

- `Banking_Loans_Project.ipynb` — Data cleaning, analysis, and visualizations.
- `app.py` — Streamlit dashboard.
- `Banking_Loans_CLEANED_Mid_Project.csv` — Cleaned dataset used by the dashboard.
- `Banking_Loans_App.jpg` — Image used on the dashboard overview page.

## Dashboard

The Streamlit application includes four sections:

- Portfolio Overview
- Portfolio Insights
- Portfolio Deep Dive
- Executive Summary

These sections present the main findings through summaries and interactive charts.

## How to Run the App

Install the required libraries:

```bash
python -m pip install streamlit pandas plotly
```

Then run the application:

```bash
streamlit run app.py
```

Make sure the dataset filename in the project folder matches the filename used in the application code.

## Conclusion

This project provided practical experience in data cleaning, exploratory analysis, visualization, and building an interactive dashboard using a banking loans dataset.