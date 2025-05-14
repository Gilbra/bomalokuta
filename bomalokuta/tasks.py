# task.py
import logging
from .models import TaskRecord
import uuid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import uuid
import logging
from celery import shared_task
from .models import TaskRecord
from .utils import send_to_chatglm  # ou ce que tu utilises comme moteur IA

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def analyze_text_task(self, task_id, text):
    logger.info(f"[Celery] Texte reçu pour analyse (task_id={task_id}): {text}")
    try:
        result = send_to_chatglm(text)  # Fonction externe d’analyse IA
        TaskRecord.objects.filter(task_id=task_id).update(
            status="done",  # ou "success" selon ton schéma
            result={"message": result}
        )
    except Exception as e:
        logger.error(f"[Celery] Erreur pendant l’analyse : {e}")
        TaskRecord.objects.filter(task_id=task_id).update(
            status="failure",
            result={"error": str(e)}
        )


@shared_task
def analyze_text_async(text):
    task_id = str(uuid.uuid4())
    TaskRecord.objects.create(
        task_id=task_id,
        status="queued",
        result=None
    )
    analyze_text_task.delay(task_id, text)
    return task_id  # Ce retour est optionnel
