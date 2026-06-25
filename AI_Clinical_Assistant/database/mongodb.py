from pymongo import MongoClient
import streamlit as st

client = MongoClient(
    st.secrets["MONGODB_URI"]
)

db = client["clinical_ai_db"]

doctors = db["doctors"]
patients = db["patients"]
consultations = db["consultations"]
reports = db["reports"]
voice_embeddings = db["voice_embeddings"]