import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st
import pandas as pd

from database.mongodb import consultations

st.title(
    "📁 Patient Records"
)

if "doctor_id" not in st.session_state:

    st.error(
        "Please login first."
    )

    st.stop()

doctor_id = st.session_state[
    "doctor_id"
]

records = list(

    consultations.find(
        {
            "doctor_id":
            doctor_id
        }
    )

)

if not records:

    st.info(
        "No consultations found."
    )

    st.stop()

table_data = []

for record in records:

    table_data.append({

        "Consultation ID":
        record.get(
            "consultation_id"
        ),

        "Patient ID":
        record.get(
            "patient_id"
        ),

        "Patient Name":
        record.get(
            "patient_name"
        ),

        "Prediction":
        record.get(
            "prediction"
        ),

        "Date":
        str(
            record.get(
                "created_at"
            )
        )[:19]
    })

df = pd.DataFrame(
    table_data
)

st.dataframe(
    df,
    use_container_width=True
)

selected_consultation = st.selectbox(

    "Select Consultation",

    [
        r[
            "consultation_id"
        ]
        for r in records
    ]

)

if st.button(
    "Open Report"
):

    selected_record = next(

        r
        for r in records

        if r[
            "consultation_id"
        ]
        ==
        selected_consultation

    )

    st.session_state[
        "selected_report"
    ] = selected_record

    st.switch_page(
        "pages/6_Report_Editor.py"
    )

