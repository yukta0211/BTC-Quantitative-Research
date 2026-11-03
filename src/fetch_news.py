import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent

# Load API key
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    raise ValueError("TAVILY_API_KEY not found. Check your .env file.")

# Tavily API
url = "https://api.tavily.com/search"

payload = {
    "api_key": API_KEY,
    "query": "Bitcoin BTC cryptocurrency market news",
    "topic": "news",
    "days": 7,
    "max_results": 10,
    "include_answer": True
}

print("Fetching recent Bitcoin news...")

response = requests.post(
    url,
    json=payload,
    timeout=30
)

response.raise_for_status()
data = response.json()

# Extract news articles
articles = []

for item in data.get("results", []):
    articles.append({
        "title": item.get("title"),
        "url": item.get("url"),
        "content": item.get("content"),
        "published_date": item.get("published_date"),
        "score": item.get("score")
    })

news_df = pd.DataFrame(articles)

# Save results
output_folder = ROOT / "data" / "raw"
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "btc_news.csv"
news_df.to_csv(output_file, index=False)

print("\nNEWS COLLECTION COMPLETE")
print("Articles collected:", len(news_df))
print("Saved to:", output_file)

if not news_df.empty:
    print("\nHEADLINES:")
    for index, row in news_df.iterrows():
        print(f"\n{index + 1}. {row['title']}")
        print("Source:", row["url"])
        print("Summary:", row["content"])
else:
    print("No articles returned. Try a different search query.")

