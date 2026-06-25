import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(
        str(ROOT_DIR)
    )

import streamlit as st

st.set_page_config(layout="wide")

st.title("🏥 Doctor Dashboard")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Patients",
        "124"
    )

with col2:
    st.metric(
        "Consultations",
        "256"
    )

with col3:
    st.metric(
        "Reports",
        "240"
    )

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.info(
        "Start a new consultation with a patient."
    )

    st.page_link(
        "pages/4_Record_Consultation.py",
        label="🎤 Start Consultation"
    )

with col2:

    st.info(
        "View patient history and reports."
    )

    st.page_link(
        "pages/5_Patient_Records.py",
        label="📁 Patient Records"
    )

st.markdown("---")

st.subheader("Doctor Profile")

st.write("Doctor ID: DOC001")
st.write("Name: Dr Kavya")
st.write("Specialization: General Medicine")