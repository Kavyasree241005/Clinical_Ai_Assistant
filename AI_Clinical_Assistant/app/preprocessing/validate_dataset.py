
import json
from pathlib import Path

INPUT_PATH = Path("data/processed/merged_dataset.json")
OUTPUT_PATH = Path("data/processed/validated_dataset.json")

required_fields = [
    "conversation_id",
    "conversation",
    "clinical_entities",
    "possible_condition"
]

valid_records = []
invalid_count = 0

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

for record in dataset:

    try:
        # Check required fields
        for field in required_fields:
            if field not in record:
                raise ValueError(f"Missing field: {field}")

        # Check symptoms
        symptoms = record["clinical_entities"].get("symptoms", [])

        if not symptoms:
            raise ValueError("Missing symptoms")

        # Check disease label
        if not record["possible_condition"]:
            raise ValueError("Missing possible condition")

        valid_records.append(record)

    except Exception as e:
        invalid_count += 1

print(f"\nValid records: {len(valid_records)}")
print(f"Invalid records removed: {invalid_count}")

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(valid_records, f, indent=4)

print(f"Validated dataset saved to: {OUTPUT_PATH}")

