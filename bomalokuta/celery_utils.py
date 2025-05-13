# bomalokuta/celery_utils.py
import logging
from .tasks import analyze_text_async, analyze_text_task
from .models import TaskRecord
import uuid
from django.conf import settings

logger = logging.getLogger(__name__)

def safe_analyze_text(text):
    """
    Tente d'exécuter l'analyse via Celery. Si Redis est indisponible, exécute localement en fallback.
    """
    task_id = str(uuid.uuid4())

    # Création du TaskRecord avant exécution
    TaskRecord.objects.create(
        task_id=task_id,
        input_text=text,
        status='pending',
        result=None
    )

    # Cas avec Celery actif (Redis dispo)
    if not settings.USE_CELERY_FALLBACK:
        try:
            analyze_text_task.delay(task_id, text)
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            logger.warning(f"[Fallback forcé] Échec de Celery, passage en local : {e}")

    # Cas fallback local
    try:
        result = analyze_text_async.run(text)
        TaskRecord.objects.filter(task_id=task_id).update(
            status="success",
            result={"message": result}
        )
        return {"task_id": task_id, "status": "done", "result": result}
    except Exception as e:
        logger.error(f"Erreur d'analyse locale fallback : {e}")
        TaskRecord.objects.filter(task_id=task_id).update(
            status="failure",
            result={"error": str(e)}
        )
        return {"task_id": task_id, "status": "error", "result": str(e)}
