import medspacy
from medspacy.ner import TargetRule
import re
import logging

logging.getLogger().setLevel(logging.ERROR)

nlp = medspacy.load()

target_matcher = nlp.get_pipe("medspacy_target_matcher")

# Symptom list
symptom_rules = [

    TargetRule("fever", "SYMPTOM"),
    TargetRule("headache", "SYMPTOM"),
    TargetRule("cough", "SYMPTOM"),
    TargetRule("chest pain", "SYMPTOM"),
    TargetRule("shortness of breath", "SYMPTOM"),
    TargetRule("nausea", "SYMPTOM"),
    TargetRule("vomiting", "SYMPTOM"),
    TargetRule("diarrhea", "SYMPTOM"),
    TargetRule("fatigue", "SYMPTOM"),
    TargetRule("dizziness", "SYMPTOM"),
    TargetRule("sore throat", "SYMPTOM"),
    TargetRule("body aches", "SYMPTOM")

]

medication_rules = [

    TargetRule("paracetamol", "MEDICATION"),
    TargetRule("ibuprofen", "MEDICATION"),
    TargetRule("amoxicillin", "MEDICATION"),
    TargetRule("azithromycin", "MEDICATION"),
    TargetRule("metformin", "MEDICATION")

]

target_matcher.add(
    symptom_rules +
    medication_rules
)

DURATION_PATTERN = re.compile(
    r'(\d+|one|two|three|four|five|six|seven|eight|nine|ten)\s*(day|days|week|weeks|month|months|hour|hours|year|years)',
    re.IGNORECASE
)

AGE_PATTERN = re.compile(
    r'(\d+)\s*(years|year)'
)

BODY_PARTS = {

    "head",
    "chest",
    "abdomen",
    "stomach",
    "back",
    "leg",
    "arm",
    "throat",
    "neck",
    "shoulder",
    "knee",
    "ankle",
    "eye",
    "ear"

}


def extract_clinical_entities(text: str):

    text = text.lower()

    doc = nlp(text)

    symptoms = []
    medications = []

    for ent in doc.ents:

        if ent.label_ == "SYMPTOM":
            symptoms.append(ent.text)

        elif ent.label_ == "MEDICATION":
            medications.append(ent.text)

    ###################################################
    # Duration extraction
    ###################################################

    duration = None

    duration_match = DURATION_PATTERN.search(text)

    if duration_match:

        number = duration_match.group(1)
        unit = duration_match.group(2)

        if (
            number.lower() not in ["one", "1"]
            and not unit.endswith("s")
        ):
            unit += "s"

        duration = f"{number} {unit}"

    ###################################################
    # Body part extraction
    ###################################################

    body_part = None

    words = text.split()

    for part in BODY_PARTS:

        if part in words:
            body_part = part
            break

    ###################################################
    # Severity extraction
    ###################################################

    severity = None

    if any(
        x in text
        for x in
        ["severe", "extreme", "unbearable"]
    ):
        severity = "severe"

    elif any(
        x in text
        for x in
        ["moderate", "bad"]
    ):
        severity = "moderate"

    elif any(
        x in text
        for x in
        ["mild"]
    ):
        severity = "mild"

    ###################################################
    # Age extraction
    ###################################################

    age = None

    age_match = AGE_PATTERN.search(text)

    if age_match:
        age = age_match.group(1)

    ###################################################
    # Gender extraction
    ###################################################

    gender = None

    if "male" in text:
        gender = "male"

    elif "female" in text:
        gender = "female"

    ###################################################
    # Final output
    ###################################################

    return {

        "symptoms":
        list(set(symptoms)),

        "duration":
        duration,

        "severity":
        severity,

        "body_part":
        body_part,

        "medications":
        list(set(medications)),

        "age":
        age,

        "gender":
        gender

    }