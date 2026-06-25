import os
import json
import numpy as np

from resemblyzer import VoiceEncoder
from resemblyzer import preprocess_wav


MODEL_DIR = "models/voice_db"

EMBEDDINGS_FILE = (
    f"{MODEL_DIR}/doctor_embeddings.json"
)

SIMILARITY_THRESHOLD = 0.80


class VoiceIdentifier:

    def __init__(self):

        os.makedirs(
            MODEL_DIR,
            exist_ok=True
        )

        print(
            "Loading Resemblyzer model..."
        )

        self.encoder = VoiceEncoder()

        self.doctor_profiles = (
            self._load_profiles()
        )

    def _load_profiles(self):

        if os.path.exists(
            EMBEDDINGS_FILE
        ):

            with open(
                EMBEDDINGS_FILE,
                "r"
            ) as f:

                data = json.load(f)

            return {

                k: np.array(v)

                for k, v in data.items()

            }

        return {}

    def _save_profiles(self):

        data = {

            k: v.tolist()

            for k, v in
            self.doctor_profiles.items()

        }

        with open(
            EMBEDDINGS_FILE,
            "w"
        ) as f:

            json.dump(
                data,
                f
            )

    def _get_embedding(
            self,
            audio_path
    ):

        wav = preprocess_wav(
            audio_path
        )

        embedding = (
            self.encoder.embed_utterance(
                wav
            )
        )

        return embedding

    def enroll_doctor(
            self,
            name,
            audio_paths
    ):

        embeddings = []

        for path in audio_paths:

            emb = self._get_embedding(
                path
            )

            embeddings.append(
                emb
            )

        avg_emb = np.mean(
            embeddings,
            axis=0
        )

        self.doctor_profiles[name] = (
            avg_emb
        )

        self._save_profiles()

        print(
            f"Doctor '{name}' enrolled successfully."
        )

    def identify_speaker(
            self,
            audio_chunk_path
    ):

        if not self.doctor_profiles:

            return (
                "Patient",
                0.0
            )

        chunk_emb = self._get_embedding(
            audio_chunk_path
        )

        best_name = "Patient"

        best_score = 0.0

        for name, profile_emb in (

            self.doctor_profiles.items()

        ):

            score = np.dot(

                chunk_emb,
                profile_emb

            ) / (

                np.linalg.norm(chunk_emb)
                *
                np.linalg.norm(profile_emb)

            )

            if score > best_score:

                best_score = float(score)

                best_name = name

        if best_score < (
            SIMILARITY_THRESHOLD
        ):

            return (
                "Patient",
                best_score
            )

        return (
            best_name,
            best_score
        )