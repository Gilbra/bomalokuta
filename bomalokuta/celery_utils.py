# bomalokuta/celery_utils.py

import uuid
import logging

from django.conf import settings

from .models import TaskRecord
from .tasks import analyze_text_async
from .utils import analyze_fake_news  # IA via Gradio ou local

logger = logging.getLogger(__name__)


def safe_analyze_text(text, user=None):
    """
    Lance une tâche d’analyse en async (Celery) ou local (fallback).
    Crée un TaskRecord immédiatement pour suivre la tâche.
    """
    task_id = str(uuid.uuid4())

    # Enregistrement anticipé dans TaskRecord
    TaskRecord.objects.create(
        task_id=task_id,
        input_text=text,
        status="pending",
        user=user
    )

    # ✅ Mode Celery (asynchrone avec broker)
    if not settings.USE_CELERY_FALLBACK:
        try:
            analyze_text_async.apply_async(args=[text], task_id=task_id)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            logger.warning(f"[Celery Fallback] Échec de l’envoi async, passage au mode local : {e}")

    # ✅ Mode Fallback (exécution directe dans le thread)
    try:
        result = analyze_fake_news(text)
        TaskRecord.objects.filter(task_id=task_id).update(
            status="done",
            result={"message": result}
        )
        return {"task_id": task_id, "status": "done", "result": {"message": result}}

    except Exception as e:
        logger.error(f"[Fallback Error] Erreur locale : {e}")
        TaskRecord.objects.filter(task_id=task_id).update(
            status="failure",
            result={"error": str(e)}
        )
        return {"task_id": task_id, "status": "error", "result": {"error": str(e)}}
