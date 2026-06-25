
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "phi3"


def generate_response(prompt):

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "top_p": 0.85,
            "top_k": 20,
            "repeat_penalty": 1.2,
            "num_predict": 120
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload
    )

    result = response.json()

    return result["response"]
