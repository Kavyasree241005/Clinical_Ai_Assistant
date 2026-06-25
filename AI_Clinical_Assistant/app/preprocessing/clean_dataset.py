
import json
from pathlib import Path

INPUT_PATH = Path("data/processed/validated_dataset.json")
OUTPUT_PATH = Path("data/processed/cleaned_dataset.json")

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

cleaned_records = []

for record in dataset:

    try:
        clinical_entities = record.get("clinical_entities", {})

        symptoms = clinical_entities.get("symptoms", [])

        # Skip records with empty symptoms
        if not symptoms:
            continue

        # Normalize symptoms
        symptoms = [
            str(symptom).lower().strip()
            for symptom in symptoms
            if symptom
        ]

        # Normalize optional fields
        duration = str(
            clinical_entities.get("duration", "")
        ).lower().strip()

        severity = str(
            clinical_entities.get("severity", "")
        ).lower().strip()

        body_part = str(
            clinical_entities.get("body_part", "")
        ).lower().strip()

        medications = clinical_entities.get("medications", [])

        medications = [
            str(med).lower().strip()
            for med in medications
            if med
        ]

        # Update normalized fields
        clinical_entities["symptoms"] = symptoms
        clinical_entities["duration"] = duration
        clinical_entities["severity"] = severity
        clinical_entities["body_part"] = body_part
        clinical_entities["medications"] = medications

        record["clinical_entities"] = clinical_entities

        cleaned_records.append(record)

    except Exception as e:
        print(f"Error processing record: {e}")

print(f"\nTotal cleaned records: {len(cleaned_records)}")

# Save cleaned dataset
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(cleaned_records, f, indent=4)

print(f"Cleaned dataset saved to: {OUTPUT_PATH}")
