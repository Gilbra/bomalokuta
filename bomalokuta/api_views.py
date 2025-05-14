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
    - Lance l’analyse via Celery ou fallback local
    - Crée un TaskRecord (optionnellement lié à un utilisateur)
    - Retourne un objet avec task_id, status, et éventuellement result ou error
    """
    permission_classes = [AllowAny]

    def post(self, request):
        text = request.data.get("text", "").strip()
        if not text:
            return Response({"error": "Texte requis"}, status=status.HTTP_400_BAD_REQUEST)

        # Récupération de l'utilisateur connecté (optionnel)
        user = None
        if request.user.is_authenticated:
            try:
                user = CustomUser.objects.get(user_associated=request.user)
            except CustomUser.DoesNotExist:
                logger.warning(f"[Analyze] Utilisateur connecté introuvable : {request.user.username}")
        
        # Lance l’analyse via safe_analyze_text
        response = safe_analyze_text(text, user=user)

        # Construction de la réponse
        payload = {
            "task_id": response["task_id"],
            "status": response["status"]
        }

        if response["status"] == "done":
            payload["result"] = response["result"]
        elif response["status"] == "error":
            payload["error"] = response["result"]

        code = status.HTTP_202_ACCEPTED if response["status"] == "queued" else status.HTTP_200_OK
        return Response(payload, status=code)


class AnalyzeResultAPIView(APIView):
    """
    GET /api/analyze/{task_id}/
    - Renvoie l’état d’une tâche et son résultat final si disponible
    - Peut interroger TaskRecord (fallback local) ou AsyncResult (Celery)
    """
    permission_classes = [AllowAny]

    def get(self, request, task_id):
        if settings.USE_CELERY_FALLBACK:
            logger.debug(f"[Fallback] Lecture TaskRecord pour {task_id}")
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

        # Sinon, lecture depuis Celery (mode production)
        res = AsyncResult(task_id)
        if not res.ready():
            return Response({
                "task_id": task_id,
                "status": "pending"
            }, status=status.HTTP_200_OK)

        # Résultat prêt (renvoyé par la tâche Celery)
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
