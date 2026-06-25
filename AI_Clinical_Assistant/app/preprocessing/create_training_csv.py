
import json
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

INPUT_PATH = Path("data/processed/cleaned_dataset.json")

TRAIN_OUTPUT = Path("data/processed/training_dataset.csv")
TEST_OUTPUT = Path("data/processed/test_dataset.csv")

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    dataset = json.load(f)

rows = []

for record in dataset:

    clinical_entities = record.get("clinical_entities", {})

    symptoms = clinical_entities.get("symptoms", [])
    duration = clinical_entities.get("duration", "")
    severity = clinical_entities.get("severity", "")
    body_part = clinical_entities.get("body_part", "")

    disease = record.get("possible_condition", "")

    # Create ML feature text
    symptoms_text = " ".join(symptoms)

    full_text = f"""
    {symptoms_text}
    {duration}
    {severity}
    {body_part}
    """

    full_text = " ".join(full_text.split()).lower()

    rows.append({
        "symptoms_text": full_text,
        "disease": disease
    })

# Create DataFrame
df = pd.DataFrame(rows)

print("\nDataset Preview:")
print(df.head())

print(f"\nTotal rows: {len(df)}")

# Train-test split
train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    random_state=42
)

# Save CSV files
train_df.to_csv(TRAIN_OUTPUT, index=False)
test_df.to_csv(TEST_OUTPUT, index=False)

print(f"\nTraining dataset saved to: {TRAIN_OUTPUT}")
print(f"Test dataset saved to: {TEST_OUTPUT}")

