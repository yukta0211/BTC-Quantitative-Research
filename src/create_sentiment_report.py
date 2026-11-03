import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Load collected data
tweets = pd.read_csv(ROOT / "data/processed/tweets_clean.csv")
print("Available columns:", tweets.columns.tolist())
sentiment = pd.read_csv(ROOT / "data/processed/hourly_sentiment.csv")
news = pd.read_csv(ROOT / "data/raw/btc_news.csv")

# Calculate sentiment statistics
avg_sentiment = tweets["compound"].mean()
positive = (tweets["compound"] > 0.05).mean() * 100
negative = (tweets["compound"] < -0.05).mean() * 100
neutral = 100 - positive - negative

if avg_sentiment > 0.05:
    overall = "Positive"
elif avg_sentiment < -0.05:
    overall = "Negative"
else:
    overall = "Neutral"

earliest = pd.to_datetime(tweets["created_at"], utc=True).min()
latest = pd.to_datetime(tweets["created_at"], utc=True).max()

# Extract news headlines
headlines = "\n".join(
    f"- {row['title']}"
    for _, row in news.head(10).iterrows()
)

report = f"""
# BITCOIN (BTC) — SENTIMENT OUTLOOK

## 1. Executive Summary

The collected X/Twitter posts indicate an overall {overall.lower()}
sentiment towards Bitcoin.

The average VADER compound sentiment score is {avg_sentiment:.4f}.

This suggests that the sampled discussion is slightly
{"positive" if avg_sentiment > 0 else "negative" if avg_sentiment < 0 else "neutral"}.

## 2. Twitter Sentiment Analysis

- Total tweets analysed: {len(tweets)}
- Average sentiment score: {avg_sentiment:.4f}
- Positive tweets: {positive:.2f}%
- Negative tweets: {negative:.2f}%
- Neutral tweets: {neutral:.2f}%
- First tweet: {earliest}
- Last tweet: {latest}

## 3. Recent Bitcoin News

The Tavily search returned {len(news)} news articles.

Key headlines:

{headlines}

## 4. Market Interpretation

Recent news highlights concerns surrounding the Binance security
incident, market liquidations and Bitcoin price weakness.

These developments may contribute to uncertainty and cautious
market sentiment.

However, the Twitter sample shows only a short snapshot of public
discussion and should not be treated as a representation of the
entire cryptocurrency market.

## 5. Data Limitations

- The collected 1,000 tweets cover approximately five hours.
- The sample does not provide the intended 180-day coverage.
- Only four hourly sentiment observations overlap with the
  historical Bitcoin price dataset.
- Sentiment findings are therefore exploratory.
- News is used for contextual interpretation, not as a
  predictive model feature.

## 6. Outlook

The available information suggests a cautious market environment.
The short Twitter sample indicates slightly positive/negative/neutral
discussion, while recent news highlights several market risks.

This outlook is descriptive and is not investment advice.
"""

# Correct the outlook wording dynamically
report = report.replace(
    "slightly positive/negative/neutral",
    f"slightly {overall.lower()}"
)

output = ROOT / "reports" / "sentiment_outlook.md"
output.write_text(report, encoding="utf-8")

print("Sentiment outlook generated successfully!")
print("Saved to:", output)

