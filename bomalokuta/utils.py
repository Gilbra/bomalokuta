import time
import requests
import logging

logger = logging.getLogger(__name__)

# ✅ Assure-toi que l'URL est correcte (pas de faute de frappe)
HUGGINGFACE_API = "https://gilbra-bomalkt.hf.space/predict"

def send_to_chatglm(prompt, retries=3, delay=3):
    for i in range(retries):
        try:
            logger.info(f"Tentative {i+1} d'envoi à l'IA.")
            response = requests.post(
                HUGGINGFACE_API,
                json={"data": [prompt]},
                timeout=60
            )
            response.raise_for_status()  # Lève une HTTPError si code 4xx ou 5xx
            result = response.json()
            logger.debug(f"Réponse IA : {result}")
            return result["data"][0]  # Normalement, c'est le texte généré
        except requests.exceptions.HTTPError as http_err:
            logger.warning(f"Erreur HTTP ({response.status_code}) à la tentative {i+1}: {http_err}")
        except Exception as e:
            logger.warning(f"Erreur à la tentative {i+1}: {e}")
        
        # Attendre avant de réessayer (sauf dernière tentative)
        if i < retries - 1:
            time.sleep(delay)

    # Après toutes les tentatives échouées
    logger.error(f"IA indisponible après {retries} tentatives.")
    return "⚠️ L'IA est temporairement indisponible. Veuillez réessayer plus tard."
