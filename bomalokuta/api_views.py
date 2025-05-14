# bomalokuta/api_views.py

import logging
from django.conf import settings
from celery.result import AsyncResult
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import TaskRecordSerializer
from .models import TaskRecord, CustomUser, Message, Reaction
from .celery_utils import safe_analyze_text

logger = logging.getLogger(__name__)

class AnalyzeAPIView(APIView):
    """
    POST /api/analyze/
    - lance l'analyse (via Celery ou fallback local)
    - crée toujours un TaskRecord
    - renvoie toujours {"task_id": "...", "status": "..."}
    """
    permission_classes = [AllowAny]

    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response({"error": "Texte requis"}, status=status.HTTP_400_BAD_REQUEST)

        # safe_analyze_text crée le TaskRecord et déclenche la tâche
        # Associe l'utilisateur si connecté
        user = None
        if request.user.is_authenticated:
            try:
                user = CustomUser.objects.get(user_associated=request.user)
            except CustomUser.DoesNotExist:
                pass  # ou logguer l'erreur

        response = safe_analyze_text(text, user=user)
        
        # response a toujours "task_id" et "status"
        # si status == "queued", la tâche est en attente ; sinon "done" ou "error"
        code = status.HTTP_202_ACCEPTED if response["status"] == "queued" else status.HTTP_200_OK
        payload = {
            "task_id": response["task_id"],
            "status": response["status"]
        }
        # si fini immédiatement, on peut aussi renvoyer le résultat
        if response["status"] == "done":
            payload["result"] = response["result"]
        elif response["status"] == "error":
            payload["error"] = response["result"]

        return Response(payload, status=code)

class AnalyzeResultAPIView(APIView):
    """
    GET /api/analyze/{task_id}/
    - rend l'état et le résultat via TaskRecord (fallback) ou AsyncResult (Celery)
    """
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        # mode fallback local : on lit la table TaskRecord
        if settings.USE_CELERY_FALLBACK:
            logger.debug(f"[Fallback] consultation TaskRecord {task_id}")
            try:
                task = TaskRecord.objects.get(task_id=task_id)
            except TaskRecord.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Tâche introuvable."},
                    status=status.HTTP_404_NOT_FOUND
                )
            return Response({
                "task_id": task.task_id,
                "status": task.status,
                "result": task.result
            }, status=status.HTTP_200_OK)

        # mode Celery : on interroge directement le broker pour l'état
        res = AsyncResult(task_id)
        if not res.ready():
            return Response({"task_id": task_id, "status": "pending"}, status=status.HTTP_200_OK)

        # prêt : res.result contient la valeur renvoyée par la tâche analyze_text_async
        return Response({
            "task_id": task_id,
            "status": "done",
            "result": res.result
        }, status=status.HTTP_200_OK)

class TaskListAPIView(ListAPIView):
    """
    GET /api/tasks/
    Renvoie toutes les tâches enregistrées (analyses), triées par date.
    """
    queryset = TaskRecord.objects.all().order_by('-created_at')
    serializer_class = TaskRecordSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
   
class UserTaskListAPIView(ListAPIView):
    serializer_class = TaskRecordSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskRecord.objects.filter(user__user_associated=self.request.user).order_by('-created_at')

class MyTasksAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            custom_user = CustomUser.objects.get(user_associated=request.user)
        except CustomUser.DoesNotExist:
            return Response({"error": "Profil utilisateur manquant"}, status=400)

        tasks = TaskRecord.objects.filter(user=custom_user).order_by('-created_at')
        serialized = [
            {
                "task_id": t.task_id,
                "status": t.status,
                "result": t.result,
                "created_at": t.created_at
            } for t in tasks
        ]
        return Response(serialized)
 
class ReactionAPIView(APIView):
    """
    POST /api/reaction/
    Enregistre ou met à jour une réaction d'un CustomUser sur un Message donné.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message_id = request.data.get('message_id')
        reaction = request.data.get('reaction')
        try:
            custom_user = CustomUser.objects.get(user_associated=request.user)
            message = Message.objects.get(pk=message_id)
            Reaction.objects.update_or_create(
                user=custom_user,
                message=message,
                defaults={'reaction': reaction}
            )
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Message.DoesNotExist:
            return Response({'status': 'error', 'message': 'Message non trouvé.'},
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Erreur ajout réaction: {e}")
            return Response({'status': 'error', 'message': str(e)},
                            status=status.HTTP_400_BAD_REQUEST)
