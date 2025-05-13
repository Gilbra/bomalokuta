from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import TaskRecord
from .serializers import AnalyzeRequestSerializer
from .tasks import analyze_text_task
import uuid

class AnalyzeView(APIView):
    #permission_classes = [IsAuthenticated]
    authentication_classes = [] #[SessionAuthentication]  # ou [] si tu veux aucune auth
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = AnalyzeRequestSerializer(data=request.data)
        if serializer.is_valid():
            text = serializer.validated_data['text']
            task_id = str(uuid.uuid4())
            TaskRecord.objects.create(task_id=task_id, input_text=text)
            analyze_text_task.delay(task_id, text)
            return Response({"task_id": task_id}, status=202)
        return Response(serializer.errors, status=400)

class ResultView(APIView):
    def get(self, request, task_id):
        try:
            task = TaskRecord.objects.get(task_id=task_id)
            return Response({
                "task_id": task.task_id,
                "status": task.status,
                "result": task.result
            }, status=200)
        except TaskRecord.DoesNotExist:
            return Response({"error": "Tâche introuvable."}, status=404)
