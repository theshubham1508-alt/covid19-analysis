import pandas as pd 
import numpy as np

df = pd.read_csv("owid-covid-data.csv", parse_dates=['date'])

cols = [
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

df = df[cols].copy()

df = df[~df["iso_code"].str.startswith("OWID")]

df = df.dropna(subset=["continent"])

df = df.drop_duplicates(subset=["location", "date"])

df = df.sort_values(["location", "date"]).reset_index(drop=True)

df["new_cases"] = df["new_cases"].clip(lower=0)

df["new_deaths"] = df["new_deaths"].clip(lower=0)

cum_cols = [
    "total_cases",
    "total_deaths",
    "total_vaccinations",
    "people_vaccinated",
    "people_fully_vaccinated",
    "people_fully_vaccinated_per_hundred"
]
for c in cum_cols:
    df[c] = df.groupby("location")[c].ffill()

df[["new_cases", "new_deaths"]] = df[["new_cases", "new_deaths"]].fillna(0)

df["cases_7d"] = df.groupby("location")["new_cases"].transform(
    lambda s: s.rolling(7, min_periods=1).mean()
)
df["deaths_7d"] = df.groupby("location")["new_deaths"].transform(
    lambda s: s.rolling(7, min_periods=1).mean()
)

df["cfr_percent"] = np.where(
    df["total_cases"] > 0,
    df["total_deaths"] / df["total_cases"] * 100,
    np.nan
)
df.to_csv("covid_clean.csv", index=False)


print("Clean shape:", df.shape)

print("Countries:", df["location"].nunique())

print(
    "Date range:",
    df["date"].min().date(),
    "to",
    df["date"].max().date()
)

print(
    df.isnull().sum()[
        ["total_cases", "total_deaths", "cases_7d"]
    ]
)