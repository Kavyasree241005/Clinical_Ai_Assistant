
import spacy

nlp = spacy.load("en_core_web_sm")

# Symptom normalization dictionary
SYMPTOM_MAP = {
    "feverish": "fever",
    "chills": "fever",
    "shivering": "fever",
    "tiredness": "fatigue",
    "dizzy": "dizziness",
    "vomiting": "vomit",
    "throwing": "vomit",
    "coughing": "cough",
    "breathlessness": "shortness_breath",
    "breathing": "shortness_breath",
    "stomachache": "stomach_pain",
    "tummy": "stomach",
    "migraine": "headache"
}

def preprocess_text(text):

    text = str(text)

    doc = nlp(text)

    cleaned_tokens = []

    for token in doc:

        if token.is_stop:
            continue

        if token.is_punct:
            continue

        if token.is_space:
            continue

        word = token.lemma_.lower().strip()

        # Apply synonym normalization
        if word in SYMPTOM_MAP:
            word = SYMPTOM_MAP[word]

        if word:
            cleaned_tokens.append(word)

    return " ".join(cleaned_tokens)

