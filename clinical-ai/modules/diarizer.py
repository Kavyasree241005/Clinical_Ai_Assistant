from pyannote.audio import Pipeline
import torch
import soundfile as sf
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class SpeakerDiarizer:

    def __init__(self):

        print("Loading Pyannote diarization model...")

        HF_TOKEN = os.getenv("HF_TOKEN")

        if HF_TOKEN is None:
            raise ValueError(
                "HF_TOKEN not found in .env file"
            )

        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-3.1",
            token=HF_TOKEN
        )

    def diarize(self, audio_path):

        waveform, sample_rate = sf.read(audio_path)

        if len(waveform.shape) > 1:
            waveform = waveform.mean(axis=1)

        waveform = torch.tensor(
            waveform
        ).float()

        waveform = waveform.unsqueeze(0)

        diarization = self.pipeline(
            {
                "waveform": waveform,
                "sample_rate": sample_rate
            },
            min_speakers=2,
            max_speakers=3
        )

        segments = []

        for turn, speaker in diarization.speaker_diarization:

            segments.append({

                "speaker": speaker,

                "start": turn.start,

                "end": turn.end

            })

        return segments