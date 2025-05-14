from rest_framework import serializers

from .models import *
class AnalyzeRequestSerializer(serializers.Serializer):
    text = serializers.CharField()

class TaskRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskRecord
        fields = ['task_id', 'input_text', 'status', 'result', 'created_at']