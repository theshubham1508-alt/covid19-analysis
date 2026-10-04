# COVID-19 Trend Analysis & Case Forecasting

## 📌 Project Overview

This project analyzes COVID-19 data to identify trends in cases and deaths,
perform SQL-based analysis, and compare forecasting models.

## 🛠️ Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- SQL / SQLite
- Scikit-learn
- Statsmodels
- Excel

## 📊 Project Workflow

1. Data Loading & Validation
2. Data Cleaning
3. SQL Analysis
4. Exploratory Data Analysis
5. Vaccination vs Death Analysis
6. ARIMA Forecasting
7. Random Forest Forecasting
8. Excel Report

## 🔍 Analysis Performed

- COVID-19 case and death trends
- Top 10 countries by total cases
- India monthly cases
- 7-day rolling average
- Peak COVID-19 days
- Continent-wise analysis
- Vaccination vs deaths
- ARIMA forecasting
- Random Forest forecasting

## 🤖 Model Results

| Model | RMSE | MAPE |
|---|---:|---:|
| ARIMA | 2303.7 | 59.5% |
| Random Forest | 196.3 | 7.1% |
| Baseline lag_1 | 242.8 | 8.8% |

Random Forest performed better than the baseline on the test data.

## 📁 Project Files

- `clean.py` - Data cleaning
- `sql.py` - SQL analysis
- `eda.py` - Exploratory Data Analysis
- `vaccination.py` - Vaccination analysis
- `arima.py` - ARIMA forecasting
- `ml.py` - Random Forest forecasting
- `covid_report.xlsx` - Excel report
- `covid_clean.csv` - Cleaned dataset
- `images/` - Generated visualizations

## 👨‍💻 Author

Shubham
