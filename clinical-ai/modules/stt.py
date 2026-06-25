from faster_whisper import WhisperModel
import numpy as np

class ClinicalSTT:
    def __init__(self, model_size="medium"):
        print(f"Loading Whisper {model_size}...")
        # Use "cuda" if you have GPU, else "cpu"
        self.model = WhisperModel(model_size,device="cpu",compute_type="int8",download_root=r"D:\intern\clinical-ai\models\whisper")    
    def transcribe(self, audio_path: str, language: str = "en") -> dict:
        """
        Transcribe audio file. Returns dict with text and word-level timestamps.
        Set language="ta" for Tamil, "hi" for Hindi, etc.
        """
        segments, info = self.model.transcribe(
            audio_path,
            language=language,
            beam_size=5,
            word_timestamps=True
        )
        
        full_text = ""
        words_with_times = []
        
        for segment in segments:
            full_text += segment.text + " "
            if segment.words:
                for word in segment.words:
                    words_with_times.append({
                        "word": word.word,
                        "start": word.start,
                        "end": word.end
                    })
        
        return {
            "text": full_text.strip(),
            "language": info.language,
            "words": words_with_times
        }