from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import User as UserGeneral
from django.db import models

class CustomUser(models.Model):
    # Ajoutez des champs personnalisés si nécessaire
    user_associated = models.OneToOneField(UserGeneral, on_delete=models.CASCADE, related_name='custom_user_terranova', verbose_name=_('Utilisateur associé'))
    points = models.IntegerField(default=0)  # Points accumulés par l'utilisateur
    role = models.CharField(max_length=20, choices=[
        ('utilisateur', 'Utilisateur'),
        ('administrateur', 'Administrateur'),
        ('éco-influenceur', 'Éco-Influenceur'),
        ('partenaire', 'Partenaire'),
        ('municipalité', 'Municipalité'),
    ], default='utilisateur')

    def __str__(self):
        return self.username


class Dechet(models.Model):
    STATUS_CHOICES = [
        ('signalé', 'Signalé'),
        ('en_cours', 'En cours de traitement'),
        ('traité', 'Traité'),
    ]

    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='dechets/')
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='signalé')
    date_signalement = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Déchet {self.id} signalé par {self.utilisateur.username}'


class PointCollecte(models.Model):
    TYPE_CHOICES = [
        ('bac', 'Bac à déchets'),
        ('centre', 'Centre de recyclage'),
    ]

    nom = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    niveau_remplissage = models.IntegerField(default=0)  # en pourcentage
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    def __str__(self):
        return self.nom


class Evenement(models.Model):
    utilisateur = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    lieu = models.CharField(max_length=200)

    def __str__(self):
        return self.titre


class Statistique(models.Model):
    utilisateur = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dechets_signalés = models.IntegerField(default=0)
    dechets_recyclés = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Statistiques de {self.utilisateur.username}'


class Recompense(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    points = models.IntegerField()

    def __str__(self):
        return self.nom
    
class Resource(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='resources/')  # Pour les fichiers PDF, tutoriels, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ressource'
        verbose_name_plural = 'Ressources'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    auteur = models.OneToOneField(UserGeneral, on_delete=models.CASCADE, related_name='auteur_news', verbose_name=_('auteur'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Actualité'
        verbose_name_plural = 'Actualités'
        ordering = ['-created_at']

    def __str__(self):
        return self.title