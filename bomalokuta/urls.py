# bomalokuta/urls.py
from django.urls import path
from .views import home, dashboard
from .api_views import *
# déjà dans .api_views import AnalyzeAPIView, AnalyzeResultAPIView...
#from .drf_views import AnalyzeView, ResultView

app_name = 'bomalokuta'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    # API DRF
    #path('api/analyze/', AnalyzeView.as_view(), name='api_analyze'),
    #path('api/resultats/<str:task_id>/', ResultView.as_view(), name='api_result'),
    
    path('api/analyze/', AnalyzeAPIView.as_view(), name='api-analyze'),
    path('api/analyze/<str:task_id>/', AnalyzeResultAPIView.as_view(), name='api-analyze-result'),
    path('api/tasks/', TaskListAPIView.as_view(), name='api-task-list'),
    path('api/user_tasks/', UserTaskListAPIView.as_view(), name='api-user-task-list'),
    path('api/mytasks/', MyTasksAPIView.as_view(), name='api-mytasks'),
    path('api/reaction/', ReactionAPIView.as_view(), name='api-reaction'),
]
