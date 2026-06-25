
def build_soap_prompt(
    symptoms,
    duration,
    severity,
    predicted_condition
):

    return f"""
You are a clinical documentation assistant.

Generate ONLY the SOAP note.

Rules:
- Use ONLY provided information.
- Do not add symptoms.
- Do not add allergies.
- Do not add medications.
- Do not add medical history.
- Do not add differential diagnoses.
- Do not add vital signs.
- Do not use markdown.
- One sentence per section.
- Maximum 15 words per section.

Symptoms: {symptoms}
Duration: {duration}
Severity: {severity}
Condition: {predicted_condition}

Output exactly:

Subjective:
...

Objective:
No physical examination findings were provided.

Assessment:
...

Plan:
...
"""
