import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import streamlit as st

from database.doctor_db import (
    login_doctor
)

st.title("Doctor Login")

email = st.text_input(
    "Email"
)

password = st.text_input(
    "Password",
    type="password"
)

if st.button(
    "Login",
    use_container_width=True
):

    if not email or not password:

        st.error(
            "Please enter email and password."
        )

    else:

        doctor = login_doctor(
            email,
            password
        )

        if doctor:

            st.session_state[
                "doctor_id"
            ] = doctor[
                "doctor_id"
            ]

            st.session_state[
                "doctor_name"
            ] = doctor[
                "name"
            ]

            st.session_state[
                "doctor_email"
            ] = doctor[
                "email"
            ]

            st.success(
                f"Welcome Dr. {doctor['name']}"
            )

        else:

            st.error(
                "Invalid email or password."
            )