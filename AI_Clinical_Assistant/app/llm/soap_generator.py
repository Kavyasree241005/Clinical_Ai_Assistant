
import re

from app.llm.ollama_client import generate_response


def generate_soap_note(
    symptoms,
    duration,
    severity,
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
- One sentence for Assessment.
- One sentence for Plan.
- Do not add symptoms.
- Do not add medications.
- Do not add allergies.
- Do not add medical history.
- Do not add differential diagnoses.
- Do not add vital signs.
- No markdown.

Condition:
{predicted_condition}
"""

    response = generate_response(prompt)

    subjective = (
        f"Patient reports {symptoms} "
        f"for {duration} "
        f"with {severity} severity."
    )

    objective = (
        "No physical examination findings, "
        "vital signs, or laboratory data available."
    )

    assessment = (
        f"Clinical presentation is consistent with "
        f"{predicted_condition}."
    )

    plan = (
        "Recommend hydration, rest, and "
        "symptomatic management."
    )

    # Try to extract plan from LLM response
    plan_match = re.search(
        r"Plan:\s*(.*)",
        response,
        re.IGNORECASE | re.DOTALL
    )

    if plan_match:
        extracted_plan = plan_match.group(1).strip()

        if len(extracted_plan) > 10:
            plan = extracted_plan

    soap = {
        "subjective": subjective,
        "objective": objective,
        "assessment": assessment,
        "plan": plan
    }

    return soap
