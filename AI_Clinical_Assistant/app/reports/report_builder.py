from pathlib import Path

from jinja2 import (
    Environment,
    FileSystemLoader
)


def build_report(
    conversation_id,
    symptoms,
    duration,
    severity,
    predicted_condition,
    soap_note
):

    # Project Root
    BASE_DIR = Path(
        __file__
    ).resolve().parents[2]

    # Template Directory
    TEMPLATE_DIR = (
        BASE_DIR
        / "app"
        / "templates"
    )

    env = Environment(
        loader=FileSystemLoader(
            str(TEMPLATE_DIR)
        )
    )

    template = env.get_template(
        "soap_template.jinja2"
    )

    report_text = template.render(
        conversation_id=conversation_id,
        predicted_condition=predicted_condition,
        symptoms=symptoms,
        duration=duration,
        severity=severity,
        subjective=soap_note["subjective"],
        objective=soap_note["objective"],
        assessment=soap_note["assessment"],
        plan=soap_note["plan"]
    )

    return report_text