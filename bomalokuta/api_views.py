from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.throttling import UserRateThrottle
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import SessionAuthentication

from .tasks import analyze_text_async
from bomalokuta.models import *
from bomalokuta.celery_utils import safe_analyze_text
from celery.result import AsyncResult

import logging
logger = logging.getLogger(__name__)

class AnalyzeAPIView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = []

    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response({"error": "Texte requis"}, status=400)
        response = safe_analyze_text(text)

        if response["status"] == "queued":
            return Response({"task_id": response["task_id"], "status": "processing"}, status=202)
        elif response["status"] == "done":
            return Response({
                "task_id": response["task_id"],
                "status": "done",
                "result": response["result"]
            }, status=200)
        else:
            return Response({"error": response["result"]}, status=500)

class AnalyzeResultAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        if settings.USE_CELERY_FALLBACK:
            logger.info(f"Recherche de la tâche {task_id}")
            try:
                task = TaskRecord.objects.get(task_id=task_id)
                return Response({
                    "status": task.status,
                    "result": task.result
                }, status=200)
            except TaskRecord.DoesNotExist:
                return Response({"status": "error", "message": "Tâche introuvable."}, status=404)
        else:
            res = AsyncResult(task_id)
            if not res.ready():
                return Response({"status": "pending"}, status=200)
            return Response({
                "status": "done",
                "result": res.result
            }, status=200)    

class ReactionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message_id = request.data.get('message_id')
        reaction = request.data.get('reaction')
        try:
            custom_user = CustomUser.objects.get(user_associated=request.user)
            message = Message.objects.get(id=message_id)
            from .models import Reaction
            Reaction.objects.update_or_create(
                user=custom_user,
                message=message,
                defaults={'reaction': reaction}
            )
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
