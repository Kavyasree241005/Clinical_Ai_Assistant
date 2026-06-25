import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))
from database.doctor_db import register_doctor
import streamlit as st

st.title("Doctor Registration")

doctor_id = st.text_input("Doctor ID")

name = st.text_input("Doctor Name")

email = st.text_input("Email")

password = st.text_input(
    "Password",
    type="password"
)

specialization = st.text_input(
    "Specialization"
)

hospital = st.text_input(
    "Hospital"
)

phone = st.text_input(
    "Phone Number"
)

voice_files = st.file_uploader(
    "Upload Voice Samples",
    type=["wav"],
    accept_multiple_files=True
)

if st.button("Register"):

    doctor_data = {

        "doctor_id":
        doctor_id,

        "name":
        name,

        "email":
        email,

        "password":
        password,

        "specialization":
        specialization,

        "hospital":
        hospital,

        "phone":
        phone
    }

    register_doctor(
        doctor_data
    )

    st.success(
        "Doctor Registered Successfully"
    )