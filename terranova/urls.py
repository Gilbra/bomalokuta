from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

#from .fictif import *

app_name = 'terranova'

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'dechets', DechetViewSet)
router.register(r'points-collecte', PointCollecteViewSet)
router.register(r'evenements', EvenementViewSet)
router.register(r'statistiques', StatistiqueViewSet)
router.register(r'recompenses', RecompenseViewSet)

router.register(r'resources', ResourceViewSet)
router.register(r'news', NewsViewSet)

urlpatterns = [
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]