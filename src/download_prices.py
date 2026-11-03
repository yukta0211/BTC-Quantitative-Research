import yfinance as yf
from pathlib import Path

print("Downloading Bitcoin hourly price data...")

btc = yf.download(
    "BTC-USD",
    period="60d",
    interval="1h",
    auto_adjust=True
)

if btc.empty:
    print("Download failed. No data received.")
else:
    output_folder = Path("data/raw")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "btc_hourly.csv"

    btc.to_csv(output_file)

    print("\nDownload successful!")
    print(f"Total price records: {len(btc)}")
    print(f"Saved to: {output_file}")
    print("\nFirst five records:")
    print(btc.head())