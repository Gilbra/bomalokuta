# bomalokuta/utils.py

from transformers import pipeline
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
