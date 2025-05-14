# bomalokuta/utils.py

import time
import requests
import logging
import json

logger = logging.getLogger(__name__)

# ✅ Adresse correcte du Space Hugging Face
HUGGINGFACE_API = "https://gilbra-bomalkt.hf.space/run/predict"

def build_prompt(text: str) -> str:
    """
    Construit le prompt à envoyer à ChatGLM pour détecter les fake news.
    Format attendu : JSON structuré.
    """
    return f"""
            Tu es un expert en fact-checking. Analyse ce texte pour fournir :
            1. Un verdict (Vrai, Faux ou Douteux).
            2. Un score de confiance de 0 à 100.
            3. Une explication concise.
            4. Une liste de sources (URLs ou références), vide si aucune.

            Réponds **strictement** au format JSON suivant, sans rien ajouter :

            {{
            "verdict": "Vrai|Faux|Douteux",
            "score": 0-100,
            "explication": "…",
            "sources": ["…","…"]
            }}

        Texte à analyser :
        \"\"\"{text}\"\"\"
        """

def call_space(prompt: str, retries: int = 3, delay: int = 2) -> str:
    """
    Appelle le Space Gradio de Hugging Face avec le prompt donné.
    Retourne la réponse texte (JSON brut) ou une réponse d'erreur structurée.
    """
    payload = {"data": [prompt]}
    print(prompt)
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"[IA] Appel HF (tentative {attempt}/{retries})")
            resp = requests.post(HUGGINGFACE_API, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            print('++++')
            return data["data"][0]
        except requests.HTTPError as he:
            print('****')
            logger.warning(f"[IA] HTTP {resp.status_code} à la tentative {attempt}: {he}")
        except Exception as e:
            print('+-*+-*')
            logger.warning(f"[IA] Exception tentative {attempt}: {e}")
        if attempt < retries:
            time.sleep(delay)

    # Toutes les tentatives ont échoué, on retourne une réponse formatée
    logger.error("[IA] Échec définitif du Space HuggingFace")
    return json.dumps({
        "verdict": "Erreur",
        "score": 0,
        "explication": "L'IA est temporairement indisponible. Veuillez réessayer plus tard.",
        "sources": []
    })

def analyze_fake_news(text: str) -> dict:
    """
    Fonction d'analyse de fake news (entrée unique pour le backend) :
    1. Génère le prompt
    2. Envoie à Hugging Face
    3. Parse et valide le JSON reçu
    """
    print(text, flush=True)
    prompt = build_prompt(text)
    raw = call_space(prompt)
    
    try:
        result = json.loads(raw)
        if all(k in result for k in ("verdict", "score", "explication", "sources")):
            return result
        else:
            raise ValueError("Clés manquantes dans la réponse IA")
    except Exception as e:
        logger.error(f"[IA] Réponse mal formée ou invalide : {e}")
        return {
            "verdict": "Erreur",
            "score": 0,
            "explication": f"Réponse IA invalide ou mal formée : {raw}",
            "sources": []
        }
