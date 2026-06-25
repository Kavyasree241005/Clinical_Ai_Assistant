
import pandas as pd
import joblib

from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer

from app.preprocessing.text_preprocessing import preprocess_text

# Paths
TRAIN_DATA_PATH = Path("data/processed/training_dataset.csv")
VECTORIZER_OUTPUT = Path("data/models/tfidf_vectorizer.pkl")

# Load dataset
df = pd.read_csv(TRAIN_DATA_PATH)

print("\nDataset Loaded")
print(df.head())

# Preprocess text
print("\nPreprocessing text...")

df["cleaned_text"] = df["symptoms_text"].apply(preprocess_text)

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["cleaned_text"])

print("\nTF-IDF Shape:")
print(X.shape)

# Save vectorizer
VECTORIZER_OUTPUT.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(vectorizer, VECTORIZER_OUTPUT)

print(f"\nVectorizer saved to: {VECTORIZER_OUTPUT}")

