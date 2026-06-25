import sounddevice as sd
import numpy as np
import noisereduce as nr
import webrtcvad
import wave, io, struct

SAMPLE_RATE = 16000
FRAME_DURATION_MS = 30  # VAD works on 10/20/30ms frames
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION_MS / 1000)

def record_audio(duration_seconds: int, filename: str = "consultation.wav"):
    """Record from default mic for given duration."""
    print(f"Recording for {duration_seconds}s...")
    audio = sd.rec(
        int(duration_seconds * SAMPLE_RATE),
        samplerate=SAMPLE_RATE,
        channels=1,
        dtype='float32'
    )
    sd.wait()
    print("Recording done.")
    return audio.flatten()

def reduce_noise(audio: np.ndarray, sr: int = SAMPLE_RATE) -> np.ndarray:
    """Apply noisereduce for background noise removal."""
    reduced = nr.reduce_noise(y=audio, sr=sr, stationary=False)
    return reduced

def detect_speech_segments(audio: np.ndarray, sr: int = SAMPLE_RATE) -> list:
    """
    Use WebRTC VAD to detect speech frames.
    Returns list of (start_sample, end_sample) tuples.
    """
    vad = webrtcvad.Vad()
    vad.set_mode(0)  # 0-3, higher = more aggressive filtering
    
    # Convert float32 to 16-bit PCM
    pcm = (audio * 32767).astype(np.int16)
    
    segments = []
    speech_start = None
    
    for i in range(0, len(pcm) - FRAME_SIZE, FRAME_SIZE):
        frame = pcm[i:i + FRAME_SIZE]
        frame_bytes = struct.pack(f'{len(frame)}h', *frame)
        is_speech = vad.is_speech(frame_bytes, sr)
        
        if is_speech and speech_start is None:
            speech_start = i
        elif not is_speech and speech_start is not None:
            segments.append((speech_start, i))
            speech_start = None
    
    if speech_start is not None:
        segments.append((speech_start, len(pcm)))
    
    return segments

def save_wav(audio: np.ndarray, path: str, sr: int = SAMPLE_RATE):
    pcm = (audio * 32767).astype(np.int16)
    with wave.open(path, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm.tobytes())