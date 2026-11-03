import json
import pandas as pd
from pathlib import Path
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# File locations
raw_folder = Path("data/raw")
output_folder = Path("data/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Load tweets
json_file = raw_folder / "btc_tweets_180d.json"

if not json_file:
    raise FileNotFoundError("Tweet JSON file not found!")

with open(json_file, "r", encoding="utf-8") as file:
    tweets = json.load(file)

df = pd.DataFrame(tweets)

# Keep relevant columns
df = df[[
    "id", "text", "created_at",
    "like_count", "retweet_count",
    "reply_count", "view_count",
    "author_followers", "lang"
]].copy()

# Remove duplicates and non-English tweets
df = df.drop_duplicates(subset="id")
df = df[df["lang"] == "en"].copy()

# Convert timestamps to UTC
df["created_at"] = pd.to_datetime(
    df["created_at"], utc=True, errors="coerce"
)

df = df.dropna(subset=["created_at", "text"])

# Calculate sentiment
analyzer = SentimentIntensityAnalyzer()

sentiment = df["text"].apply(analyzer.polarity_scores)

df["positive"] = sentiment.apply(lambda x: x["pos"])
df["negative"] = sentiment.apply(lambda x: x["neg"])
df["neutral"] = sentiment.apply(lambda x: x["neu"])
df["compound"] = sentiment.apply(lambda x: x["compound"])

# Create hourly timestamp
df["hour"] = df["created_at"].dt.floor("h")

# Save individual processed tweets
df.to_csv(output_folder / "tweets_clean.csv", index=False)

# Aggregate sentiment by hour
hourly = df.groupby("hour").agg(
    tweet_count=("id", "count"),
    avg_sentiment=("compound", "mean"),
    positive_sentiment=("positive", "mean"),
    negative_sentiment=("negative", "mean"),
    avg_likes=("like_count", "mean"),
    avg_retweets=("retweet_count", "mean"),
    avg_views=("view_count", "mean"),
    avg_followers=("author_followers", "mean")
).reset_index()

hourly.to_csv(
    output_folder / "hourly_sentiment.csv",
    index=False
)

print("Tweet processing completed!")
print(f"Tweets processed: {len(df)}")
print(f"Hourly sentiment records: {len(hourly)}")
print("\nSentiment summary:")
print(df["compound"].describe())

print("\nFiles saved in data/processed/")

print("\nTWEET DATE COVERAGE")
print("Earliest tweet:", df["created_at"].min())
print("Latest tweet:", df["created_at"].max())

print("\nTweets per day:")
print(
    df.groupby(df["created_at"].dt.date)
    .size()
    .sort_index()
)

print("\nTweets per hour:")
print(
    df.groupby("hour")
    .size()
    .sort_index()
)