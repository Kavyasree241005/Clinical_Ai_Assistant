import sys
from pathlib import Path
from datetime import datetime

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.mongodb import (
    consultations
)

st.title(
    "📄 Report Editor"
)

if (
    "selected_report"
    not in st.session_state
):

    st.warning(
        "No report selected."
    )

    st.stop()

record = st.session_state[
    "selected_report"
]

st.subheader(
    "Patient Information"
)

st.write(
    f"Patient ID: {record['patient_id']}"
)

st.write(
    f"Patient Name: {record['patient_name']}"
)

st.write(
    f"Prediction: {record['prediction']}"
)

st.write(
    f"Consultation ID: {record['consultation_id']}"
)

st.markdown("---")

status = record.get(
    "finalized",
    False
)

if status:

    st.success(
        "✅ Report Status: FINALIZED"
    )

else:

    st.warning(
        "📝 Report Status: DRAFT"
    )

st.markdown("---")

soap = record[
    "soap_note"
]

subjective = st.text_area(
    "Subjective",
    value=soap.get(
        "subjective",
        ""
    ),
    height=120
)

objective = st.text_area(
    "Objective",
    value=soap.get(
        "objective",
        ""
    ),
    height=120
)

assessment = st.text_area(
    "Assessment",
    value=soap.get(
        "assessment",
        ""
    ),
    height=120
)

plan = st.text_area(
    "Plan",
    value=soap.get(
        "plan",
        ""
    ),
    height=150
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

###################################################
# SAVE CHANGES
###################################################

with col1:

    if st.button(
        "💾 Save Changes",
        use_container_width=True
    ):

        consultations.update_one(

            {
                "consultation_id":
                record[
                    "consultation_id"
                ]
            },

            {
                "$set":
                {
                    "soap_note":
                    {
                        "subjective":
                        subjective,

                        "objective":
                        objective,

                        "assessment":
                        assessment,

                        "plan":
                        plan
                    },

                    "last_modified":
                    datetime.now()
                }
            }

        )

        st.success(
            "Report Updated Successfully"
        )

###################################################
# FINALIZE REPORT
###################################################

with col2:

    if st.button(
        "✅ Finalize Report",
        use_container_width=True
    ):

        consultations.update_one(

            {
                "consultation_id":
                record[
                    "consultation_id"
                ]
            },

            {
                "$set":
                {
                    "finalized":
                    True,

                    "finalized_at":
                    datetime.now()
                }
            }

        )

        st.success(
            "Report Finalized Successfully"
        )

###################################################
# DOWNLOAD PDF
###################################################

with col3:

    pdf_path = record.get(
        "pdf_path"
    )

    if pdf_path and Path(pdf_path).exists():

        try:

            with open(
                pdf_path,
                "rb"
            ) as pdf_file:

                st.download_button(

                    label=
                    "⬇ Download PDF",

                    data=
                    pdf_file,

                    file_name=
                    Path(
                        pdf_path
                    ).name,

                    mime=
                    "application/pdf",

                    use_container_width=True
                )

        except FileNotFoundError:

            st.error(
                "PDF file not found."
            )

    else:

        st.warning(
            "No PDF available."
        )

st.markdown("---")

st.subheader(
    "Current Conversation"
)

if "conversation_json" in record:

    st.json(
        record[
            "conversation_json"
        ]
    )

