import json

from app.ml.predict import predict_disease

from app.llm.soap_generator import (
    generate_soap_note
)

from app.reports.report_builder import (
    build_report
)

from app.reports.pdf_generator import (
    generate_pdf
)


def run_pipeline(data):

    print("\n===== AI Clinical Assistant =====\n")

    # =========================
    # EXTRACT DATA
    # =========================

    conversation_id = data["conversation_id"]

    conversation = data.get(
        "conversation",
        []
    )

    entities = data["clinical_entities"]

    symptoms = entities.get(
        "symptoms",
        []
    )

    duration = entities.get(
        "duration",
        ""
    )

    severity = entities.get(
        "severity"
    )

    if severity is None:
        severity = "unspecified"

    # =========================
    # CREATE ML INPUT
    # =========================

    ml_input = " ".join(symptoms)

    if duration:
        ml_input += " " + duration

    if severity:
        ml_input += " " + severity

    print("\nML Input:")
    print(ml_input)

    # =========================
    # DISEASE PREDICTION
    # =========================

    prediction_result = predict_disease(
        ml_input
    )

    predicted_condition = prediction_result[
        "final_prediction"
    ]["prediction"]

    confidence = prediction_result[
        "final_prediction"
    ]["confidence"]

    print("\nPredicted Disease:")
    print(predicted_condition)

    print(
        f"Confidence: {confidence:.2f}%"
    )

    # =========================
    # SOAP NOTE GENERATION
    # =========================

    soap_note = generate_soap_note(
        symptoms=", ".join(symptoms),
        duration=duration,
        severity=severity,
        predicted_condition=predicted_condition
    )

    print("\n===== SOAP NOTE =====\n")

    for section, text in soap_note.items():

        print(section.upper())
        print(text)
        print()

    # =========================
    # REPORT BUILDING
    # =========================

    report_text = build_report(
        conversation_id=conversation_id,
        symptoms=", ".join(symptoms),
        duration=duration,
        severity=severity,
        predicted_condition=predicted_condition,
        soap_note=soap_note
    )

    # =========================
    # PDF GENERATION
    # =========================

    pdf_path = generate_pdf(
        report_text
    )

    print(
        "\nClinical report generated successfully."
    )

    # =========================
    # RETURN RESULTS
    # =========================

    return {

        "conversation_id":
        conversation_id,

        "conversation":
        conversation,

        "prediction":
        predicted_condition,

        "confidence":
        confidence,

        "soap_note":
        soap_note,

        "report_text":
        report_text,

        "pdf_path":
        pdf_path
    }


# =========================
# STANDALONE TESTING
# =========================

if __name__ == "__main__":

    with open(
        "data/input.json",
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    result = run_pipeline(
        data
    )

    print("\n===== FINAL RESULT =====\n")

    print(
        json.dumps(
            result,
            indent=4,
            default=str
        )
    )
