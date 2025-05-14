# tasks.py

import logging
from celery import shared_task

from .models import TaskRecord
from .utils import analyze_fake_news  # Ton moteur IA

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def analyze_text_task(self, task_id, text):
    """
    Tâche principale appelée avec un task_id déjà existant dans la base.
    """
    logger.info(f"[Celery] Analyse du texte (task_id={task_id}) démarrée.")
    try:
        result = analyze_fake_news(text)

        TaskRecord.objects.filter(task_id=task_id).update(
            status="done",
            result={"message": result}
        )
        logger.info(f"[Celery] Analyse terminée avec succès pour {task_id}.")

    except Exception as e:
        logger.error(f"[Celery] Échec de l’analyse pour {task_id} : {e}")
        TaskRecord.objects.filter(task_id=task_id).update(
            status="failure",
            result={"error": str(e)}
        )


@shared_task
def analyze_text_async(text):
    """
    Tâche alternative (non utilisée avec safe_analyze_text).
    Conservée ici pour compatibilité éventuelle.
    """
    from uuid import uuid4
    task_id = str(uuid4())

    TaskRecord.objects.create(
        task_id=task_id,
        input_text=text,
        status="queued",
        result=None
    )

    # Appel asynchrone de la tâche réelle
    analyze_text_task.delay(task_id, text)

    return task_id
