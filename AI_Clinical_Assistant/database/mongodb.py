from pymongo import MongoClient

client = MongoClient(
    "mongodb://localhost:27017"
)

db = client["clinical_ai_db"]

doctors = db["doctors"]

patients = db["patients"]

consultations = db["consultations"]

reports = db["reports"]

voice_embeddings = db["voice_embeddings"]