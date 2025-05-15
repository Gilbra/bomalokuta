# terranova/views.py
from rest_framework import generics, viewsets, permissions, status
from .models import *
from .serializers import *

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

def send_notification(user, message):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_user_{user.id}",
        {
            'type': 'send_notification',
            'notification': message
        }
    )
    
class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès sans authentification

class DechetViewSet(viewsets.ModelViewSet):
    queryset = Dechet.objects.all()
    serializer_class = DechetSerializer
    permission_classes = [permissions.AllowAny] #[permissions.IsAuthenticated]  # Nécessite une authentification

class DechetListView(generics.ListAPIView):
    queryset = Dechet.objects.all()
    serializer_class = DechetSerializer
    
class PointCollecteViewSet(viewsets.ModelViewSet):
    queryset = PointCollecte.objects.all()
    serializer_class = PointCollecteSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès sans authentification

class EvenementViewSet(viewsets.ModelViewSet):
    queryset = Evenement.objects.all()
    serializer_class = EvenementSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès sans authentification

class StatistiqueViewSet(viewsets.ModelViewSet):
    queryset = Statistique.objects.all()
    serializer_class = StatistiqueSerializer
    permission_classes = [permissions.IsAuthenticated]  # Nécessite une authentification

class RecompenseViewSet(viewsets.ModelViewSet):
    queryset = Recompense.objects.all()
    serializer_class = RecompenseSerializer
    permission_classes = [permissions.AllowAny]  # Permet l'accès sans authentification