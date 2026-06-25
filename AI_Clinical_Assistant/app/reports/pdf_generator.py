from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.pagesizes import (
    letter
)

OUTPUT_PATH = Path(
    "generated_reports/clinical_report.pdf"
)


def generate_pdf(report_text):

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    title_style = styles["Title"]

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]

    story = []

    lines = report_text.split("\n")

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if "AI Clinical Report" in line:

            para = Paragraph(
                f"<b>{line}</b>",
                title_style
            )

        elif (
            "Predicted Condition:" in line
            or "Symptoms:" in line
            or "Duration:" in line
            or "SOAP Note" in line
        ):

            para = Paragraph(
                f"<b>{line}</b>",
                heading_style
            )

        elif (
            "===" in line
            or "---" in line
        ):

            continue

        else:

            para = Paragraph(
                line,
                body_style
            )

        story.append(para)

        story.append(
            Spacer(1, 6)
        )

    doc.build(story)

    print(
        f"\nProfessional PDF Generated: {OUTPUT_PATH}"
    )

    return str(
        OUTPUT_PATH
    )
