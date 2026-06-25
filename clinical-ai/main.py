import os
import json
import tempfile
from datetime import datetime

import soundfile as sf
import numpy as np

from modules.preprocessor import (
    record_audio,
    reduce_noise,
    detect_speech_segments,
    save_wav
)

from modules.voice_id import VoiceIdentifier
from modules.stt import ClinicalSTT
from modules.nlp_extractor import extract_clinical_entities
import sys

sys.path.append(
    r"D:\Internship\AI_Clinical_Assistant"
)

from app.main import run_pipeline

SAMPLE_RATE = 16000


def process_audio_file(
        audio_path: str,
        doctor_name: str = None):
    print("PROCESS FUNCTION STARTED")

    from modules.diarizer import SpeakerDiarizer

    ###################################################
    # Step 1 : Load Audio
    ###################################################

    audio, sr = sf.read(
        audio_path,
        dtype="float32"
    )

    if audio.ndim > 1:

        audio = audio.mean(
            axis=1
        )

    ###################################################
    # Step 2 : Noise Reduction
    ###################################################

    print(
        "STEP 1: Reducing noise1..."
    )

    clean_audio = reduce_noise(
        audio,
        sr
    )

    ###################################################
    # Step 3 : Load Models
    ###################################################

    print(
        "STEP 2: Loading models..."
    )

    stt = ClinicalSTT(
        model_size="medium"
    )

    diarizer = SpeakerDiarizer()

    identifier = VoiceIdentifier()

    ###################################################
    # Step 4 : Speaker Diarization
    ###################################################

    print(
        "STEP 3: Running diarization..."
    )

    temp_audio = tempfile.NamedTemporaryFile(
        suffix=".wav",
        delete=False
    )

    temp_audio.close()

    save_wav(
        clean_audio,
        temp_audio.name,
        sr
    )


    diarization_segments = (
        diarizer.diarize(
            temp_audio.name
        )
    )
    print("\n===== DIARIZATION OUTPUT =====")
    for seg in diarization_segments:
        print(
            f"{seg['speaker']} | "
            f"{seg['start']:.2f} -> "
            f"{seg['end']:.2f}"
        )
    print("==============================\n")

    ###################################################
    # Step 5 : Segment-based Transcription
    ###################################################

    conversation = []
    speaker_scores = {}

    for seg in diarization_segments:

        start_time = seg["start"]
        end_time = seg["end"]

        duration = (
            end_time - start_time
        )

        # Ignore tiny segments
        if duration < 0.3:
            continue

        start_sample = int(
            start_time * sr
        )

        end_sample = int(
            end_time * sr
        )

        chunk = clean_audio[
            start_sample:end_sample
        ]

        if len(chunk) < SAMPLE_RATE:
            continue

        ###################################################
        # Save chunk
        ###################################################

        chunk_file = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        chunk_file.close()

        save_wav(
            chunk,
            chunk_file.name,
            sr
        )

        ###################################################
        # Transcribe chunk
        ###################################################

        result = stt.transcribe(
            chunk_file.name
        )

        text = result["text"].strip()

        # Ignore empty text
        if not text:

            try:
                os.unlink(
                    chunk_file.name
                )
            except:
                pass

            continue

        ###################################################
        # Identify speaker
        ###################################################

        speaker_name, confidence = (

            identifier.identify_speaker(
                chunk_file.name
            )

        )
        print(
            f"DIARIZER={seg['speaker']} "
            f"VOICE_ID={speaker_name} "
            f"SCORE={confidence:.2f}"
        )

        ###################################################
        # Final label
        ###################################################

        if speaker_name != "Patient":

            final_speaker = (
                speaker_name
            )

        else:

            final_speaker = (
                "Patient"
            )

        ###################################################
        # Save conversation
        ###################################################

        diarizer_speaker = seg["speaker"]

        if diarizer_speaker not in speaker_scores:
            speaker_scores[
                 diarizer_speaker
            ] = []

        speaker_scores[
            diarizer_speaker
        ].append(
            confidence
        )

        conversation.append({
            "speaker":
            diarizer_speaker,
            "text":
            text
        })

        print(

            f"[{diarizer_speaker}] "
            f"({confidence:.2f}) : "
            f"{text}"

        )

        ###################################################
        # Cleanup
        ###################################################

        try:
            os.unlink(
                chunk_file.name
            )
        except:
            pass

    ###################################################
    # Cleanup temp audio
    ###################################################
    print("\n===== SPEAKER AVERAGES =====")

    for speaker, scores in speaker_scores.items():

        avg_score = sum(scores) / len(scores)

        print(
            f"{speaker} -> "
            f"{avg_score:.3f}"
        )

    print("============================\n")
    speaker_avg_scores = {}

    for speaker, scores in speaker_scores.items():
        speaker_avg_scores[speaker] = (
             sum(scores) / len(scores)

    )

    doctor_cluster = max(
        speaker_avg_scores,
        key=speaker_avg_scores.get

    )

    print(
        f"DOCTOR CLUSTER = {doctor_cluster}"
    )
    try:
        os.unlink(
            temp_audio.name
        )
    except:
        pass
    
    for item in conversation:
        if item["speaker"] == doctor_cluster:
            item["speaker"] = "Doctor"
        else:
            item["speaker"] = "Patient"

    ###################################################
    # Step 6 : NLP Extraction
    ###################################################

    print(
        "Extracting clinical entities..."
    )

    full_text = " ".join(

        [
            x["text"]
            for x in conversation
        ]

    )

    entities = extract_clinical_entities(
        full_text
    )

    print(
        f"Found: {entities['symptoms']}"
    )

    ###################################################
    # Final JSON
    ###################################################

    conversation_json = {

        "conversation_id":
        f"C{datetime.now().strftime('%H%M%S')}",

        "conversation":
        conversation,

        "clinical_entities":
        entities

    }

    return {

        "conversation_json":
        conversation_json

    }

def process_consultation(
        audio_path):

    result = process_audio_file(
        audio_path
    )

    print(
        "\n================================="
    )

    print(
        "Starting Clinical AI Module..."
    )

    print(
        "=================================\n"
    )

    clinical_result = run_pipeline(

        result[
            "conversation_json"
        ]

    )

    clinical_result[
        "conversation_json"
    ] = result[
        "conversation_json"
    ]

    print(
        "\n================================="
    )

    print(
        "Clinical AI Processing Complete"
    )

    print(
        "=================================\n"
    )

    return clinical_result


def enroll_new_doctor(
        name: str,
        sample_paths: list):

    identifier = VoiceIdentifier()

    identifier.enroll_doctor(
        name,
        sample_paths
    )

    print(
        f"Enrolled: {name}"
    )


if __name__ == "__main__":

    print("MAIN STARTED")

    import sys

    if len(sys.argv) < 2:

        print("\nUsage:")

        print(
            "python main.py enroll 'Dr Smith' sample1.wav sample2.wav sample3.wav"
        )

        print(
            "python main.py process consultation.wav"
        )

        exit()

    command = sys.argv[1]

    if command == "enroll":

        name = sys.argv[2]

        samples = sys.argv[3:]

        enroll_new_doctor(
            name,
            samples
        )

    
    elif command == "process":

        audio_file = sys.argv[2]

        result = process_consultation(
        audio_file
        )

        print(
        "\n===== FINAL RESULT =====\n"
        )

        print(
            json.dumps(
               result,
               indent=4,
               default=str
            )
        )
