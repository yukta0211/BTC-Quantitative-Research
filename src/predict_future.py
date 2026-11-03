import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor

ROOT = Path(__file__).resolve().parent.parent
data_path = ROOT / "data" / "processed" / "btc_merged.csv"

df = pd.read_csv(data_path)

df["hour"] = pd.to_datetime(df["hour"], utc=True)
df = df.sort_values("hour").reset_index(drop=True)

# Feature engineering
df["return_1h"] = df["close"].pct_change(1)
df["return_2h"] = df["close"].pct_change(2)
df["return_3h"] = df["close"].pct_change(3)
df["return_6h"] = df["close"].pct_change(6)
df["return_12h"] = df["close"].pct_change(12)
df["return_24h"] = df["close"].pct_change(24)

df["volatility_6h"] = df["return_1h"].rolling(6).std()
df["volatility_24h"] = df["return_1h"].rolling(24).std()

features = [
    "return_1h",
    "return_2h",
    "return_3h",
    "return_6h",
    "return_12h",
    "return_24h",
    "volatility_6h",
    "volatility_24h"
]

# Create historical targets
for h in range(1, 6):
    df[f"target_{h}h"] = df["close"].shift(-h) / df["close"] - 1

training_data = df.dropna(
    subset=features + [f"target_{h}h" for h in range(1, 6)]
)

X_train = training_data[features]

# Latest available feature row
latest = df.dropna(subset=features).iloc[[-1]]
X_latest = latest[features]

current_price = latest["close"].iloc[0]
current_time = latest["hour"].iloc[0]

results = []

for h in range(1, 6):

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, training_data[f"target_{h}h"])

    predicted_return = model.predict(X_latest)[0]

    predicted_price = current_price * (1 + predicted_return)

    results.append({
        "Horizon": f"n+{h}",
        "Forecast_Time": current_time + pd.Timedelta(hours=h),
        "Predicted_Return": predicted_return,
        "Predicted_Price_USD": predicted_price
    })

results_df = pd.DataFrame(results)

print("\nCURRENT BTC PRICE:", current_price)
print("LATEST DATA TIME:", current_time)

print("\nFUTURE BTC FORECAST")
print(results_df.to_string(index=False))

output_path = ROOT / "reports" / "btc_forecast.csv"
results_df.to_csv(output_path, index=False)

print("\nForecast saved to:", output_path)