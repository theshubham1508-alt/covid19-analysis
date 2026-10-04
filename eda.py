import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

os.makedirs("images", exist_ok=True)

sns.set_style("whitegrid")

df = pd.read_csv("covid_clean.csv", parse_dates=["date"])


world = df.groupby("date")[["new_cases", "new_deaths"]].sum()

world["cases_7d"] = world["new_cases"].rolling(7).mean()

plt.figure(figsize=(11, 5))

plt.plot(
    world.index,
    world["cases_7d"]
)

plt.title("World - Daily New Cases (7-day average)")
plt.xlabel("Date")
plt.ylabel("Cases")

plt.tight_layout()

plt.savefig(
    "images/world_cases.png",
    dpi=150
)

plt.show()


countries = [
    "India",
    "United States",
    "Brazil",
    "United Kingdom"
]

sub = df[df["location"].isin(countries)].copy()

sub["cases_7d_pm"] = (
    sub["cases_7d"] /
    sub["population"] *
    1_000_000
)

plt.figure(figsize=(11, 5))

sns.lineplot(
    data=sub,
    x="date",
    y="cases_7d_pm",
    hue="location"
)

plt.title("Daily Cases per Million (7-day avg)")
plt.xlabel("Date")
plt.ylabel("Cases per million")

plt.tight_layout()

plt.savefig(
    "images/country_compare.png",
    dpi=150
)

plt.show()

latest = (
    df.sort_values("date")
      .groupby("location")
      .tail(1)
)

top10 = latest.nlargest(
    10,
    "total_cases"
)

plt.figure(figsize=(10, 5))

sns.barplot(
    data=top10,
    x="total_cases",
    y="location"
)

plt.title("Top 10 Countries by Total Cases")
plt.xlabel("Total cases")
plt.ylabel("")

plt.tight_layout()

plt.savefig(
    "images/top10.png",
    dpi=150
)

plt.show()


corr_cols = [
    "total_cases",
    "total_deaths",
    "people_fully_vaccinated_per_hundred",
    "population"
]

plt.figure(figsize=(7, 5))

sns.heatmap(
    latest[corr_cols].corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "images/heatmap.png",
    dpi=150
)

plt.show()

print("EDA complete!")
print("4 charts saved in images folder.")