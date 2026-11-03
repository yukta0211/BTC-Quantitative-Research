import pandas as pd
from pathlib import Path

# Load datasets
prices = pd.read_csv(
    "data/raw/btc_hourly.csv",
    header=[0, 1],
    index_col=0
)

sentiment = pd.read_csv(
    "data/processed/hourly_sentiment.csv"
)

# Clean price columns
prices.columns = prices.columns.get_level_values(0)
prices = prices.reset_index()

prices = prices.rename(columns={
    prices.columns[0]: "hour",
    "Close": "close",
    "Open": "open",
    "High": "high",
    "Low": "low",
    "Volume": "volume"
})

prices["hour"] = pd.to_datetime(prices["hour"], utc=True)
sentiment["hour"] = pd.to_datetime(sentiment["hour"], utc=True)

# Merge hourly data
merged = pd.merge(
    prices,
    sentiment,
    on="hour",
    how="left"
)

# Missing sentiment means no tweets were collected that hour
merged["tweet_count"] = merged["tweet_count"].fillna(0)

merged.to_csv(
    "data/processed/btc_merged.csv",
    index=False
)

print("Merge completed!")
print("Total hourly price records:", len(merged))
print("Hours with tweets:", (merged["tweet_count"] > 0).sum())
print("Hours without tweets:", (merged["tweet_count"] == 0).sum())

print("\nMerged dataset preview:")
print(merged.head())

print("\nDate range:")
print(merged["hour"].min(), "to", merged["hour"].max())