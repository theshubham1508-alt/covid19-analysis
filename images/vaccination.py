import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("covid_clean.csv", parse_dates=["date"])

latest = (
    df.sort_values("date")
      .groupby("location")
      .tail(1)
      .copy()
)

latest = latest.dropna(
    subset=[
        "people_fully_vaccinated_per_hundred",
        "population",
        "total_deaths"
    ]
)

latest = latest[latest["population"] > 1_000_000]

latest["deaths_per_million"] = (
    latest["total_deaths"]
    / latest["population"]
    * 1_000_000
)

corr = latest[
    "people_fully_vaccinated_per_hundred"
].corr(
    latest["deaths_per_million"]
)

print(
    "Correlation (vaccination vs deaths per million):",
    round(corr, 2)
)

latest["vax_group"] = pd.cut(
    latest["people_fully_vaccinated_per_hundred"],
    bins=[0, 30, 60, 100],
    labels=[
        "Low (<30%)",
        "Medium (30-60%)",
        "High (>60%)"
    ]
)

print(
    latest.groupby(
        "vax_group",
        observed=True
    )["deaths_per_million"]
    .median()
    .round(0)
)

plt.figure(figsize=(9, 6))

sns.scatterplot(
    data=latest,
    x="people_fully_vaccinated_per_hundred",
    y="deaths_per_million",
    hue="continent"
)

plt.title("Vaccination vs Deaths per Million")
plt.xlabel("Fully vaccinated per 100 people")
plt.ylabel("Deaths per million")

plt.tight_layout()

plt.savefig(
    "images/vax_vs_deaths.png",
    dpi=150
)

plt.show()

print("Vaccination analysis complete!")