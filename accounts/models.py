# accounts/models.py
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    avatar = models.ImageField(upload_to='user_profiles/', null=True, blank=True, verbose_name=_('Image de profil'), help_text=_('L\'image de profil de l\'utilisateur.'))
    phone = models.CharField(max_length=25, blank=True, null=True, verbose_name=_("Télephone"))
    email_verified = models.BooleanField(default=False)
    email_validation_token = models.CharField(max_length=64, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)