from rest_framework import serializers

class AnalyzeRequestSerializer(serializers.Serializer):
    text = serializers.CharField()
