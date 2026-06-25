
import joblib
import numpy as np

from pathlib import Path

from app.preprocessing.text_preprocessing import preprocess_text

# =========================
# PROJECT ROOT
# =========================

BASE_DIR = Path(__file__).resolve().parents[2]

# =========================
# LOAD TF-IDF VECTORIZER
# =========================

VECTORIZER_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "tfidf_vectorizer.pkl"
)

vectorizer = joblib.load(
    VECTORIZER_PATH
)

# =========================
# LOAD MODELS
# =========================

LR_MODEL_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "logistic_regression.pkl"
)

RF_MODEL_PATH = (
    BASE_DIR
    / "data"
    / "models"
    / "random_forest.pkl"
)

lr_model = joblib.load(
    LR_MODEL_PATH
)

rf_model = joblib.load(
    RF_MODEL_PATH
)

print("\nModels Loaded Successfully")

# =========================
# PREDICTION FUNCTION
# =========================

def predict_disease(symptoms_text):

    # -------------------------
    # PREPROCESS TEXT
    # -------------------------

    cleaned_text = preprocess_text(
        symptoms_text
    )

    print("\nCleaned Text:")
    print(cleaned_text)

    # -------------------------
    # TF-IDF VECTOR
    # -------------------------

    vector = vectorizer.transform(
        [cleaned_text]
    )

    # =========================
    # LOGISTIC REGRESSION
    # =========================

    lr_prediction = (
        lr_model.predict(vector)[0]
    )

    lr_probabilities = (
        lr_model.predict_proba(vector)[0]
    )

    lr_confidence = np.max(
        lr_probabilities
    )

    # =========================
    # RANDOM FOREST
    # =========================

    rf_prediction = (
        rf_model.predict(vector)[0]
    )

    rf_probabilities = (
        rf_model.predict_proba(vector)[0]
    )

    rf_confidence = np.max(
        rf_probabilities
    )

    # =========================
    # FINAL PREDICTION LOGIC
    # =========================

    if lr_prediction == rf_prediction:

        final_prediction = (
            lr_prediction
        )

        final_confidence = max(
            lr_confidence,
            rf_confidence
        )

        agreement = True

    else:

        agreement = False

        if rf_confidence > lr_confidence:

            final_prediction = (
                rf_prediction
            )

            final_confidence = (
                rf_confidence
            )

        else:

            final_prediction = (
                lr_prediction
            )

            final_confidence = (
                lr_confidence
            )

    # =========================
    # RETURN RESULTS
    # =========================

    return {

        "cleaned_text":
        cleaned_text,

        "logistic_regression": {

            "prediction":
            lr_prediction,

            "confidence":
            round(
                lr_confidence * 100,
                2
            )
        },

        "random_forest": {

            "prediction":
            rf_prediction,

            "confidence":
            round(
                rf_confidence * 100,
                2
            )
        },

        "final_prediction": {

            "prediction":
            final_prediction,

            "confidence":
            round(
                final_confidence * 100,
                2
            ),

            "models_agree":
            agreement
        }
    }


# =========================
# MAIN
# =========================

if __name__ == "__main__":

    print(
        "\n===== Clinical Disease Prediction =====\n"
    )

    user_input = input(
        "Enter symptoms: "
    )

    results = predict_disease(
        user_input
    )

    print(
        "\n===== Prediction Results ====="
    )

    print(
        "\nLogistic Regression Prediction:"
    )

    print(
        f"Disease: "
        f"{results['logistic_regression']['prediction']}"
    )

    print(
        f"Confidence: "
        f"{results['logistic_regression']['confidence']}%"
    )

    print(
        "\nRandom Forest Prediction:"
    )

    print(
        f"Disease: "
        f"{results['random_forest']['prediction']}"
    )

    print(
        f"Confidence: "
        f"{results['random_forest']['confidence']}%"
    )

    print(
        "\n===== FINAL PREDICTION ====="
    )

    print(
        f"Disease: "
        f"{results['final_prediction']['prediction']}"
    )

    print(
        f"Confidence: "
        f"{results['final_prediction']['confidence']}%"
    )

    print(
        f"Models Agree: "
        f"{results['final_prediction']['models_agree']}"
    )
