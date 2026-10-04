import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error
)


df = pd.read_csv(
    "covid_clean.csv",
    parse_dates=["date"]
)

data = df[
    df["location"] == "India"
][["date", "cases_7d"]].copy()


for lag in [1, 2, 3, 7, 14]:
    data["lag_" + str(lag)] = data["cases_7d"].shift(lag)

data["roll_14"] = (
    data["cases_7d"]
    .shift(1)
    .rolling(14)
    .mean()
)


data["dayofweek"] = data["date"].dt.dayofweek
data["month"] = data["date"].dt.month

data = data.dropna().reset_index(drop=True)


features = [
    "lag_1",
    "lag_2",
    "lag_3",
    "lag_7",
    "lag_14",
    "roll_14",
    "dayofweek",
    "month"
]

X = data[features]
y = data["cases_7d"]

X_train = X[:-30]
X_test = X[-30:]

y_train = y[:-30]
y_test = y[-30:]


rf = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)

rf.fit(X_train, y_train)
pred = rf.predict(X_test)

base = X_test["lag_1"]

def scores(actual, predicted):

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predicted
        )
    )

    mask = actual > 0

    mape = (
        mean_absolute_percentage_error(
            actual[mask],
            predicted[mask]
        ) * 100
    )

    return round(rmse, 1), round(mape, 1)


rf_rmse, rf_mape = scores(
    y_test,
    pred
)

b_rmse, b_mape = scores(
    y_test,
    base
)

print(
    "Baseline (lag_1) RMSE:",
    b_rmse,
    " MAPE:",
    b_mape,
    "%"
)

print(
    "Random Forest RMSE:",
    rf_rmse,
    " MAPE:",
    rf_mape,
    "%"
)

pd.DataFrame([
    {
        "model": "Baseline lag_1 (1-day ahead)",
        "RMSE": b_rmse,
        "MAPE_percent": b_mape
    },
    {
        "model": "Random Forest (1-day ahead)",
        "RMSE": rf_rmse,
        "MAPE_percent": rf_mape
    }
]).to_csv(
    "results_ml.csv",
    index=False
)

imp = pd.Series(
    rf.feature_importances_,
    index=features
).sort_values()

print("\nFeature Importance:")
print(imp.round(3))


plt.figure(figsize=(8, 4))

imp.plot(
    kind="barh"
)

plt.title("Feature Importance")

plt.tight_layout()

plt.savefig(
    "images/feature_importance.png",
    dpi=150
)

plt.show()


plt.figure(figsize=(11, 5))

plt.plot(
    data["date"][-30:],
    y_test.values,
    label="Actual"
)

plt.plot(
    data["date"][-30:],
    pred,
    label="Random Forest",
    linestyle="--"
)

plt.title(
    "India - Actual vs Predicted (last 30 days)"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "images/rf_actual_vs_pred.png",
    dpi=150
)

plt.show()

print("Random Forest ML complete!")