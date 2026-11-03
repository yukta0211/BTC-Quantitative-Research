import pandas as pd
import numpy as np
from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Project paths
ROOT = Path(__file__).resolve().parent.parent
data_path = ROOT / "data" / "processed" / "btc_merged.csv"

# Load data
df = pd.read_csv(data_path)

df["hour"] = pd.to_datetime(df["hour"], utc=True)
df = df.sort_values("hour").reset_index(drop=True)

# Feature engineering: historical price movements
df["return_1h"] = df["close"].pct_change(1)
df["return_2h"] = df["close"].pct_change(2)
df["return_3h"] = df["close"].pct_change(3)
df["return_6h"] = df["close"].pct_change(6)
df["return_12h"] = df["close"].pct_change(12)
df["return_24h"] = df["close"].pct_change(24)

df["volatility_6h"] = df["return_1h"].rolling(6).std()
df["volatility_24h"] = df["return_1h"].rolling(24).std()

# Predict future returns for 1 to 5 hours
for h in range(1, 6):
    df[f"target_{h}h"] = df["close"].shift(-h) / df["close"] - 1

# Select input features
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

targets = [f"target_{h}h" for h in range(1, 6)]

# Remove rows with missing values
df = df.dropna(subset=features + targets).copy()

X = df[features]
y = df[targets]

# Chronological 80:20 split
split = int(len(df) * 0.8)

# Leave a 5-hour gap to prevent overlapping target leakage
X_train = X.iloc[:split - 5]
X_test = X.iloc[split:]

y_train = y.iloc[:split - 5]
y_test = y.iloc[split:]

# Train a separate model for each horizon
results = []
trading_returns = None
for h in range(1, 6):

    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=5,
        random_state=42
    )

    model.fit(X_train, y_train[f"target_{h}h"])

    predictions = model.predict(X_test)
    actual = y_test[f"target_{h}h"]

    if h == 1:
        # Trading signal: long or short
        signals = np.sign(predictions)
    
        # Calculate strategy returns
        transaction_cost = 0.0005
    
        position_changes = np.abs(
            np.diff(signals, prepend=0)
        )
    
        trading_returns = (
            signals * actual.values
            - transaction_cost * position_changes
        )

    mae = mean_absolute_error(actual, predictions)
    rmse = np.sqrt(mean_squared_error(actual, predictions))

    results.append({
        "Horizon": f"{h} hour(s)",
        "MAE": mae,
        "RMSE": rmse
    })
        # Naive baseline: predict zero future return
    baseline_predictions = np.zeros(len(actual))

    baseline_mae = mean_absolute_error(
        actual, baseline_predictions
    )

    baseline_rmse = np.sqrt(
        mean_squared_error(actual, baseline_predictions)
    )

    results[-1]["Baseline MAE"] = baseline_mae
    results[-1]["Baseline RMSE"] = baseline_rmse

# Calculate financial performance metrics
if trading_returns is not None:

    returns = np.array(trading_returns)

    # Sharpe Ratio
    if np.std(returns) != 0:
        sharpe_ratio = (
            np.mean(returns) / np.std(returns)
        ) * np.sqrt(8760)
    else:
        sharpe_ratio = 0

    # Sortino Ratio
    downside_returns = np.minimum(returns, 0)
    downside_deviation = np.sqrt(
        np.mean(downside_returns ** 2)
    )

    if downside_deviation != 0:
        sortino_ratio = (
            np.mean(returns) / downside_deviation
        ) * np.sqrt(8760)
    else:
        sortino_ratio = 0

    # Maximum Drawdown
    cumulative_returns = np.cumprod(1 + returns)

    running_max = np.maximum.accumulate(
        np.insert(cumulative_returns, 0, 1)
    )[1:]

    drawdowns = (
        cumulative_returns - running_max
    ) / running_max

    max_drawdown = np.min(drawdowns)

    # Display results
    print("\nFINANCIAL PERFORMANCE METRICS")
    print(f"Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Sortino Ratio: {sortino_ratio:.4f}")
    print(f"Maximum Drawdown: {max_drawdown:.4%}")

    # Save metrics
    metrics = pd.DataFrame([{
        "Sharpe Ratio": sharpe_ratio,
        "Sortino Ratio": sortino_ratio,
        "Maximum Drawdown": max_drawdown
    }])

    metrics.to_csv(
        ROOT / "reports" / "financial_metrics.csv",
        index=False
    )

    print("\nFinancial metrics saved!")

# Display evaluation
results_df = pd.DataFrame(results)

print("\nMODEL EVALUATION")
print(results_df.to_string(index=False))

# Save results
output_path = ROOT / "reports" / "model_evaluation.csv"
results_df.to_csv(output_path, index=False)

print("\nEvaluation saved to:", output_path)