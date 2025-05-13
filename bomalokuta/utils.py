# utils.py
import requests

HUGGINGFACE_API = "https://gilbra-bomalkt.hf.space/predict"

def send_to_chatglm(prompt):
    try:
        response = requests.post(
            HUGGINGFACE_API,
            json={"data": [prompt]},
            timeout=60
        )
        response.raise_for_status()
        result = response.json()
        return result["data"][0]
    except Exception as e:
        return f"Erreur IA : {str(e)}"
