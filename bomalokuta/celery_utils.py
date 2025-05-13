# bomalokuta/celery_utils.py

import logging
import uuid
from django.conf import settings
from .tasks import analyze_text_async, analyze_text_task
from .models import TaskRecord

logger = logging.getLogger(__name__)

def safe_analyze_text(text):
    """
    Tente d'exécuter l'analyse via Celery. Si Redis est indisponible ou désactivé,
    exécute localement (fallback). Le résultat est toujours lié à un TaskRecord.
    """
    task_id = str(uuid.uuid4())

    # Création initiale du TaskRecord
    task_record = TaskRecord.objects.create(
        task_id=task_id,
        input_text=text,
        status='pending',
        result=None
    )

    # Tentative de dispatch via Celery (Redis actif)
    if not settings.USE_CELERY_FALLBACK:
        try:
            analyze_text_task.delay(task_id, text)
            logger.info(f"Tâche {task_id} envoyée à Celery.")
            return {"task_id": task_id, "status": "queued"}
        except Exception as e:
            logger.warning(f"[Celery ÉCHEC] Tâche {task_id} - fallback local activé : {e}")

    # Fallback local si Celery désactivé ou en erreur
    try:
        result = analyze_text_async.run(text)

        # Mise à jour du TaskRecord
        task_record.status = 'success'
        task_record.result = {"message": result}
        task_record.save(update_fields=["status", "result"])

        logger.info(f"Tâche {task_id} exécutée en local avec succès.")
        return {"task_id": task_id, "status": "done", "result": result}
    except Exception as e:
        logger.error(f"[Fallback LOCAL ÉCHEC] Tâche {task_id} : {e}")

        task_record.status = 'failure'
        task_record.result = {"error": str(e)}
        task_record.save(update_fields=["status", "result"])

        return {"task_id": task_id, "status": "error", "result": str(e)}
