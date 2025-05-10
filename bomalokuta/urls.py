# bomalokuta/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from bomalokuta.views import *

app_name = 'bomalokuta'

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
    path('submit/', analyze_text_view, name='analyze_text'),

    path('add_reaction/', add_reaction, name='add_reaction'),
]
