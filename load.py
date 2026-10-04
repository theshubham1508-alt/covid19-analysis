import pandas as pd
import numpy as np
import warnings 

warnings.filterwarnings("ignore")
df = pd.read_csv("owid-covid-data.csv", parse_dates=['date'])

print(df.columns.tolist()[:10])
print("Shape:", df.shape)
print(df.head())
df.info()
print(df.isnull().sum().sort_values(ascending=False).head(10))

needed = [
    "iso_code",
    "continent",
    "location",
    "date",
    "total_cases",
    "new_cases",
    "total_deaths",
    "new_deaths",
    "total_vaccinations",
    "people_vaccinated",
    "people_fully_vaccinated",
    "people_fully_vaccinated_per_hundred",
    "population"
]

missing = [c for c in needed if c not in df.columns]

print("Missing columns:", missing)