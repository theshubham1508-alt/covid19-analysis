import sqlite3
import pandas as pd

df = pd.read_csv("covid_clean.csv")

conn = sqlite3.connect("covid.db")
df.to_sql("covid", conn, if_exists="replace", index=False)

queries = {}

queries["q1_top10"] = """
SELECT location,
    MAX(total_cases) AS total_cases,
    MAX(total_deaths) AS total_deaths,
    ROUND(MAX(total_deaths) * 100.0 / MAX(total_cases), 2) AS cfr_percent
FROM covid
GROUP BY location
ORDER BY total_cases DESC
LIMIT 10;
"""

queries["q2_india_monthly"] = """
SELECT SUBSTR(date, 1, 7) AS month,
    SUM(new_cases) AS cases,
    SUM(new_deaths) AS deaths
FROM covid
WHERE location = 'India'
GROUP BY month
ORDER BY month;
"""

queries["q3_india_7d"] = """
SELECT SUBSTR(date, 1, 10) AS date,
    new_cases,
    ROUND(
        AVG(new_cases) OVER (
            ORDER BY date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 0
    ) AS avg_7d
FROM covid
WHERE location = 'India'
ORDER BY date;
"""

queries["q4_peak_day"] = """
WITH ranked AS (
    SELECT location,
        date,
        new_cases,
        RANK() OVER (
            PARTITION BY location
            ORDER BY new_cases DESC
        ) AS rnk
    FROM covid
)
SELECT location,
    SUBSTR(date, 1, 10) AS peak_date,
    new_cases
FROM ranked
WHERE rnk = 1
ORDER BY new_cases DESC
LIMIT 10;
"""

queries["q5_continent"] = """
WITH latest AS (
    SELECT location,
        continent,
        MAX(total_cases) AS tc,
        MAX(total_deaths) AS td
    FROM covid
    GROUP BY location, continent
)
SELECT continent,
    SUM(tc) AS total_cases,
    SUM(td) AS total_deaths
FROM latest
GROUP BY continent
ORDER BY total_cases DESC;
"""

for name, q in queries.items():
    result = pd.read_sql(q, conn)

    print("=== " + name + " ===")
    print(result.head(10))
    print()

    result.to_csv(name + ".csv", index=False)

conn.close()

print("SQL analysis complete!")