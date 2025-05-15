# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import *
from .api_views import RegisterView, LoginView, LogoutView, ProfileUpdateView

app_name = 'accounts'

urlpatterns = [
    path('profil/<str:username>/', profile, name='profil'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('profile_update/', profile_update, name='profile_update'),
    path('verify/<uuid:token>/', verify_email, name='verify_email'),

    # Gestion du mot de passe
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # API
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/profile/', ProfileUpdateView.as_view(), name='profile_update'),
]
