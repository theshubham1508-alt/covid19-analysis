import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import (
    mean_squared_error,
    mean_absolute_percentage_error
)

df = pd.read_csv(
    "covid_clean.csv",
    parse_dates=["date"]
)

india = (
    df[df["location"] == "India"]
    .set_index("date")["cases_7d"]
)

india = india.asfreq("D").ffill()
train = india[:-30]
test = india[-30:]

model = ARIMA(
    train,
    order=(5, 1, 2)
).fit()

forecast = model.forecast(steps=30)

rmse = np.sqrt(
    mean_squared_error(test, forecast)
)

mask = test > 0

mape = (
    mean_absolute_percentage_error(
        test[mask],
        forecast[mask]
    ) * 100
)

print("ARIMA RMSE:", round(rmse, 1))
print("ARIMA MAPE:", round(mape, 1), "%")

pd.DataFrame([
    {
        "model": "ARIMA (30-day ahead)",
        "RMSE": round(rmse, 1),
        "MAPE_percent": round(mape, 1)
    }
]).to_csv(
    "results_arima.csv",
    index=False
)

plt.figure(figsize=(11, 5))

plt.plot(
    train[-90:],
    label="Train (last 90 days)"
)

plt.plot(
    test,
    label="Actual"
)

plt.plot(
    forecast,
    label="Forecast",
    linestyle="--"
)

plt.title(
    "India - ARIMA Forecast vs Actual"
)

plt.legend()

plt.tight_layout()

plt.savefig(
    "images/arima_forecast.png",
    dpi=150
)

plt.show()

print("ARIMA forecasting complete!")