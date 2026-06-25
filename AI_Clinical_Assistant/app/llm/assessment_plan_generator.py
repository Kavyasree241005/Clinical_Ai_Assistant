
from app.llm.ollama_client import generate_response


def generate_assessment_plan(
    predicted_condition
):

    prompt = f"""
You are a clinical documentation assistant.

Generate ONLY:

Assessment:
...

Plan:
...

Rules:
- Use one sentence for Assessment.
- Use one sentence for Plan.
- Do not add symptoms.
- Do not add patient history.
- Do not add medications.
- Do not add allergies.
- Do not add vitals.
- No markdown.

Condition:
{predicted_condition}
"""

    response = generate_response(prompt)

    return response.strip()
