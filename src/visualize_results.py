import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load datasets
price = pd.read_csv(
    ROOT / "data" / "processed" / "btc_merged.csv"
)

sentiment = pd.read_csv(
    ROOT / "data" / "processed" / "hourly_sentiment.csv"
)

forecast = pd.read_csv(
    ROOT / "reports" / "btc_forecast.csv"
)

price["hour"] = pd.to_datetime(price["hour"], utc=True)
sentiment["hour"] = pd.to_datetime(sentiment["hour"], utc=True)
forecast["Forecast_Time"] = pd.to_datetime(
    forecast["Forecast_Time"], utc=True
)

# Create reports folder if needed
output = ROOT / "reports"
output.mkdir(exist_ok=True)

# CHART 1: Historical BTC price
plt.figure(figsize=(12, 5))
plt.plot(price["hour"], price["close"])
plt.title("Bitcoin Historical Price")
plt.xlabel("Time")
plt.ylabel("BTC Price (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output / "btc_price_history.png")
plt.close()

# CHART 2: Hourly sentiment
plt.figure(figsize=(12, 5))
plt.plot(
    sentiment["hour"],
    sentiment["avg_sentiment"],
    marker="o"
)
plt.axhline(y=0, linestyle="--")
plt.title("Bitcoin Twitter Sentiment Over Time")
plt.xlabel("Time")
plt.ylabel("Average VADER Sentiment")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output / "btc_sentiment.png")
plt.close()

# CHART 3: Price and sentiment observations
fig, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(price["hour"], price["close"], label="BTC Price")
ax1.set_xlabel("Time")
ax1.set_ylabel("BTC Price (USD)")

ax2 = ax1.twinx()
ax2.scatter(
    sentiment["hour"],
    sentiment["avg_sentiment"],
    label="Hourly Sentiment"
)
ax2.set_ylabel("Average Sentiment")

plt.title("Bitcoin Price and Twitter Sentiment")
fig.autofmt_xdate()
fig.tight_layout()
plt.savefig(output / "btc_price_vs_sentiment.png")
plt.close()

# CHART 4: Future forecast
current_price = price["close"].iloc[-1]

forecast_times = [price["hour"].iloc[-1]] + list(
    forecast["Forecast_Time"]
)

forecast_prices = [current_price] + list(
    forecast["Predicted_Price_USD"]
)

plt.figure(figsize=(10, 5))
plt.plot(
    forecast_times,
    forecast_prices,
    marker="o"
)
plt.title("Bitcoin 5-Hour Price Forecast")
plt.xlabel("Forecast Time")
plt.ylabel("Predicted BTC Price (USD)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output / "btc_forecast.png")
plt.close()

print("All visualisations generated successfully!")
print("Charts saved in:", output)