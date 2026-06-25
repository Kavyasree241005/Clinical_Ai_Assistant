
import json
from pathlib import Path

RAW_DATA_PATH = Path("data/raw")
OUTPUT_PATH = Path("data/processed/merged_dataset.json")

all_records = []

# Read all batch files
for file in sorted(RAW_DATA_PATH.glob("batch_*.json")):
    print(f"Reading {file.name}...")

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

        if isinstance(data, list):
            all_records.extend(data)

print(f"\nTotal records merged: {len(all_records)}")

# Save merged dataset
OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(all_records, f, indent=4)

print(f"Merged dataset saved to: {OUTPUT_PATH}")

