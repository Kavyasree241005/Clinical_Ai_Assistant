import sys
from pathlib import Path
from datetime import datetime
from database.mongodb import patients
ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# Clinical AI Project
sys.path.append(
    r"D:\Internship\clinical-ai"
)

import streamlit as st

from main import (
    process_consultation
)

from database.mongodb import (
    consultations,
    reports
)

st.title(
    "🎤 Record Consultation"
)

st.markdown("---")

patient_name = st.text_input(
    "Patient Name"
)

patient_id = st.text_input(
    "Patient ID"
)

age = st.number_input(
    "Age",
    min_value=1,
    max_value=120
)

gender = st.selectbox(
    "Gender",
    [
        "Male",
        "Female",
        "Other"
    ]
)

st.markdown("---")

audio_file = st.file_uploader(
    "Upload Consultation Audio",
    type=["wav"]
)

st.markdown("---")

if st.button(
    "Generate Clinical Report",
    use_container_width=True
):

    if audio_file is None:

        st.error(
            "Please upload a WAV file."
        )

    else:

        recordings_dir = (
            ROOT_DIR
            / "recordings"
        )

        recordings_dir.mkdir(
            exist_ok=True
        )

        audio_path = (
            recordings_dir
            / "uploaded.wav"
        )

        with open(
            audio_path,
            "wb"
        ) as f:

            f.write(
                audio_file.getbuffer()
            )

        with st.spinner(
            "Processing consultation..."
        ):

            result = process_consultation(
                str(audio_path)
            )

        ###################################################
        # SAVE TO MONGODB
        ###################################################

        consultation_doc = {

            "consultation_id":
            f"CONS_{datetime.now().strftime('%Y%m%d%H%M%S')}",

            "doctor_id":
            st.session_state.get(
                "doctor_id",
                "UNKNOWN"
            ),

            "patient_id":
            patient_id,

            "patient_name":
            patient_name,

            "age":
            age,

            "gender":
            gender,

            "conversation_json":
            result[
                "conversation_json"
            ],

            "prediction":
            result[
                "prediction"
            ],

            "confidence":
            result[
                "confidence"
            ],

            "soap_note":
            result[
                "soap_note"
            ],
            
            # ADD THESE TWO
            "pdf_path":
            result["pdf_path"],

            "finalized":
            False,

            "created_at":
            datetime.now()
        }
        existing_patient = patients.find_one(
            {
            "patient_id":
            patient_id
            }
        )

        if not existing_patient:
            patients.insert_one({

        "patient_id":
        patient_id,

        "patient_name":
        patient_name,

        "age":
        age,

        "gender":
        gender,

        "doctor_id":
        st.session_state.get(
            "doctor_id"
        )
       })
          
        consultations.insert_one(
            consultation_doc
        )

        reports.insert_one({

            "doctor_id":
            st.session_state.get(
                "doctor_id",
                "UNKNOWN"
            ),

            "patient_id":
            patient_id,

            "pdf_path":
            result[
                "pdf_path"
            ],

            "created_at":
            datetime.now()
        })

        ###################################################
        # DISPLAY RESULTS
        ###################################################

        st.success(
            "Clinical Report Generated Successfully"
        )

        st.markdown("---")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Predicted Disease",
                result[
                    "prediction"
                ]
            )

        with col2:

            st.metric(
                "Confidence",
                f"{result['confidence']}%"
            )

        st.markdown("---")

        soap = result[
            "soap_note"
        ]

        st.subheader(
            "SOAP Note"
        )

        st.info(
            soap[
                "subjective"
            ]
        )

        st.warning(
            soap[
                "objective"
            ]
        )

        st.success(
            soap[
                "assessment"
            ]
        )

        st.write(
            "### Plan"
        )

        st.write(
            soap[
                "plan"
            ]
        )

        st.markdown("---")

        st.subheader(
            "Conversation"
        )

        st.json(
            result[
                "conversation_json"
            ]
        )

        st.markdown("---")

        st.success(
            "PDF Generated Successfully"
        )

        st.code(
            result[
                "pdf_path"
            ]
        )
