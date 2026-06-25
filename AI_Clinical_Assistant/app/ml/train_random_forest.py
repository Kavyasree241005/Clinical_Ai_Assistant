
import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

from app.preprocessing.text_preprocessing import preprocess_text

# Paths
TRAIN_PATH = Path("data/processed/training_dataset.csv")
TEST_PATH = Path("data/processed/test_dataset.csv")

VECTORIZER_PATH = Path("data/models/tfidf_vectorizer.pkl")

MODEL_OUTPUT = Path("data/models/random_forest.pkl")

# Load datasets
train_df = pd.read_csv(TRAIN_PATH)
test_df = pd.read_csv(TEST_PATH)

print("\nDatasets Loaded")

# Load vectorizer
vectorizer = joblib.load(VECTORIZER_PATH)

# Preprocess text
print("\nPreprocessing text...")

train_df["cleaned_text"] = train_df["symptoms_text"].apply(preprocess_text)
test_df["cleaned_text"] = test_df["symptoms_text"].apply(preprocess_text)

# Vectorize
X_train = vectorizer.transform(train_df["cleaned_text"])
X_test = vectorizer.transform(test_df["cleaned_text"])

# Labels
y_train = train_df["disease"]
y_test = test_df["disease"]

# Initialize model
model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

# Train model
print("\nTraining Random Forest...")

model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print(f"\nAccuracy: {accuracy:.4f}")

# Report
print("\nClassification Report:\n")

print(classification_report(y_test, y_pred))

# Save model
MODEL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL_OUTPUT)

print(f"\nModel saved to: {MODEL_OUTPUT}")
