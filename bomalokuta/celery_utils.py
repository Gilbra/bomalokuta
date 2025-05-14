# bomalokuta/celery_utils.py

from .models import TaskRecord
from .tasks import analyze_text_async
from .utils import send_to_chatglm  # ton moteur local IA
from django.conf import settings
import uuid
import logging

logger = logging.getLogger(__name__)


def safe_analyze_text(text):
    if not settings.USE_CELERY_FALLBACK:
        # Utilisation de Celery
        task = analyze_text_async.delay(text)
        return {"task_id": task.id, "status": "queued"}

    # Mode fallback : traitement local immédiat
    task_id = str(uuid.uuid4())
    try:
        result = send_to_chatglm(text)
        TaskRecord.objects.create(
            task_id=task_id,
            status="done",
            result={"message": result}
        )
        return {"task_id": task_id, "status": "done", "result": {"message": result}}
    except Exception as e:
        TaskRecord.objects.create(
            task_id=task_id,
            status="failure",
            result={"error": str(e)}
        )
        return {"task_id": task_id, "status": "error", "result": {"error": str(e)}}