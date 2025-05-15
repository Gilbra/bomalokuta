from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .models import Dechet, PointCollecte, Evenement, Statistique, Recompense, Notification, SupportTicket
from .serializers import UserSerializer, DechetSerializer, PointCollecteSerializer, EvenementSerializer, StatistiqueSerializer, RecompenseSerializer, NotificationSerializer, SupportTicketSerializer

User = get_user_model()