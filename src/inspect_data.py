import json
from pathlib import Path

# Locate the downloaded JSON file
data_folder = Path("data/raw")
files = list(data_folder.glob("*.json"))

if not files:
    print("No JSON file found in data/raw!")
else:
    file_path = files[0]

    print(f"Dataset: {file_path.name}")

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    print(f"\nTotal records: {len(data)}")

    if data:
        print("\nAvailable fields:")
        print(list(data[0].keys()))

        print("\nFirst tweet:")
        print(json.dumps(data[0], indent=2, ensure_ascii=False)[:2000])