# task.py
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from celery import shared_task
from .models import TaskRecord
from .utils import send_to_chatglm  # IA via HF

@shared_task(bind=True)
def analyze_text_task(self, task_id, text):
    logger.info(f"Celery Texte reçu : {text}")
    try:
        # Appel au modèle IA externe
        result = send_to_chatglm(text)
        TaskRecord.objects.filter(task_id=task_id).update(
            status="done",  # PAS "success"
            result={"message": result}
        )

    except Exception as e:
        TaskRecord.objects.filter(task_id=task_id).update(
            status="failure",
            result={"error": str(e)}
        )

@shared_task
def analyze_text_async(text):
    """
    Tâche Celery qui appelle ChatGLM et retourne le JSON réponse.
    """
    logger.info(f"async Texte reçu : {text}")
    print("+++++")
    return send_to_chatglm(text)