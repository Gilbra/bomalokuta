# bomalokuta/utils.py

try:
    from transformers import pipeline
except ImportError:
    pipeline = None  # ou une fonction mockée
if pipeline is None:
    print("⚠️ Warning: transformers module not available. Some features may not work.")

from functools import lru_cache

@lru_cache(maxsize=1)
def get_fake_news_detector():
    """
    Charge une seule fois le modèle de détection de fake news.
    Utilise un cache pour éviter les rechargements multiples.
    """
    print("Chargement du modèle Fake News...")
    return pipeline(
        "text-classification",
        model="mrm8488/bert-tiny-fake-news",
        tokenizer="mrm8488/bert-tiny-fake-news"
    )
