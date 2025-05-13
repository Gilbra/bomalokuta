# utils.py
import time
import requests

HUGGINGFACE_API = "https://gilbra-bomalkt.hf.space/predict"

def send_to_chatglm(prompt):
    print('00000')
    return prompt
    


def send_to_chatglm_(prompt, retries=3, delay=3):
    for i in range(retries):
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
            if i < retries - 1:
                time.sleep(delay)
            else:
                return f"Erreur IA après {retries} tentatives : {str(e)}"

