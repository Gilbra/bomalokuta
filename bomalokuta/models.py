# bomalokuta/models.py

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from accounts.models import User as UserGeneral
CONTENT_TYPE_CHOICES = [
        ('article', _('Article')),
        ('video', _('Vidéo')),
        ('message', _('Message')),
        ('image', _('Image')),
        ('audio', _('Son')),
        ('pdf', _('PDF')),
    ]

class CustomUser(models.Model):
    ROLE_CHOICES = [
        ('user', _('Utilisateur')),
        ('journalist', _('Journaliste')),
        ('fact_checker', _('Vérificateur')),
        ('admin', _('Administrateur')),
    ]
    user_associated = models.OneToOneField(UserGeneral, on_delete=models.CASCADE, related_name='custom_user', verbose_name=_('Utilisateur associé'))
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user', verbose_name=_('Rôle'), help_text=_('Le rôle de cet utilisateur.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date de création de ce profil.'))
    is_active = models.BooleanField(default=True, verbose_name=_('Actif'), help_text=_('Indique si cet utilisateur est actif ou non.'))

    def __str__(self):
        return f'{self.user_associated.username} ({self.get_role_display()})'

    class Meta:
        verbose_name = _('Utilisateur personnalisé')
        verbose_name_plural = _('Utilisateurs personnalisés')
        ordering = ['created_at']

class Submission(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='submissions', verbose_name=_('Utilisateur'), help_text=_('L\'utilisateur ayant soumis ce contenu.'))
    label = models.CharField(max_length=255, verbose_name=_('Label de vérification'), help_text=_('Label à vérifier pour cette soumission.'))
    submission_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de soumission'), help_text=_('La date et l\'heure de la soumission.'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date de mise à jour'), help_text=_('La date et l\'heure de la dernière mise à jour de la soumission.'))
    verification_score = models.FloatField(null=True, blank=True, verbose_name=_('Score de vérification'), help_text=_('Le score de vérification de ce contenu.'))
    status = models.CharField(max_length=20, default='pending', verbose_name=_('Statut'), help_text=_('Le statut de la soumission (En attente, Validée, Rejetée).'))
    priority = models.CharField(max_length=20, choices=[('low', _('Faible')), ('medium', _('Moyenne')), ('high', _('Haute'))], default='medium', verbose_name=_('Priorité'), help_text=_('La priorité de la soumission.'))

    def __str__(self):
        return f'Soumission de {self.user} le {self.submission_date.strftime("%Y-%m-%d")}'

    class Meta:
        verbose_name = _('Soumission')
        verbose_name_plural = _('Soumissions')
        ordering = ['submission_date']


class SubmissionElement(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='elements', verbose_name=_('Soumission'), help_text=_('La soumission à laquelle cet élément appartient.'))
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, verbose_name=_('Type de contenu'), help_text=_('Le type de contenu (Article, Vidéo, etc.).'))
    content = models.TextField(verbose_name=_('Contenu'), help_text=_('Le contenu de l\'élément (texte, lien, etc.).'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date et l\'heure de la création de cet élément.'))
    order = models.PositiveIntegerField(default=0, verbose_name=_('Ordre d\'affichage'), help_text=_('Détermine l\'ordre d\'affichage des éléments dans la soumission.'))

    def __str__(self):
        return f'Élément de soumission ({self.content_type}) - {self.order}'

    class Meta:
        verbose_name = _('Élément de soumission')
        verbose_name_plural = _('Éléments de soumission')
        ordering = ['order', 'created_at']


class Verification(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='verifications', verbose_name=_('Soumission'), help_text=_('La soumission à vérifier.'))
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='verifications_given', verbose_name=_('Expert'), help_text=_('L\'expert ayant effectué la vérification.'))
    verification_result = models.JSONField(verbose_name=_('Résultat de la vérification'), help_text=_('Le résultat détaillé de la vérification sous format JSON.'))
    comments = models.TextField(null=True, blank=True, verbose_name=_('Commentaires'), help_text=_('Des commentaires supplémentaires de l\'expert concernant la vérification.'))
    verification_date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de vérification'), help_text=_('La date et l\'heure de la vérification.'))
    is_verified = models.BooleanField(default=False, verbose_name=_('Vérifié'), help_text=_('Indique si cette soumission a été vérifiée.'))
    next_verification_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Prochaine date de vérification'), help_text=_('La date prévue pour la prochaine vérification.'))

    def __str__(self):
        return f'Verification pour {self.submission} par {self.expert} le {self.verification_date.strftime("%Y-%m-%d")}'

    class Meta:
        verbose_name = _('Vérification')
        verbose_name_plural = _('Vérifications')
        ordering = ['verification_date']


class TextAnalysis(models.Model):
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='text_analysis', verbose_name=_('Soumission'), help_text=_('La soumission analysée.'))
    analysis_result = models.JSONField(verbose_name=_('Résultats de l\'analyse'), help_text=_('Les résultats de l\'analyse de texte sous format JSON.'))
    emotion_results = models.JSONField(verbose_name=_('Résultats des émotions'), help_text=_('Les résultats de l\'analyse des émotions sous format JSON.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date d\'analyse'), help_text=_('La date et l\'heure de la création de l\'analyse.'))

    def __str__(self):
        return f'Analyse de texte pour {self.submission}'

    class Meta:
        verbose_name = _('Analyse de texte')
        verbose_name_plural = _('Analyses de texte')
        ordering = ['created_at']


class Comment(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Soumission'), help_text=_('La soumission associée à ce commentaire.'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Utilisateur'), help_text=_('L\'utilisateur ayant rédigé ce commentaire.'))
    comment = models.TextField(verbose_name=_('Commentaire'), help_text=_('Le contenu du commentaire.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date du commentaire'), help_text=_('La date et l\'heure du commentaire.'))

    def __str__(self):
        return f'Commentaire de {self.user} sur {self.submission}'

    class Meta:
        verbose_name = _('Commentaire')
        verbose_name_plural = _('Commentaires')
        ordering = ['created_at']


class DisinformationTrend(models.Model):
    TREND_TYPE_CHOICES = [
        ('emotion', _('Émotion')),
        ('disinformation', _('Désinformation')),
    ]
    ALERT_LEVEL_CHOICES = [
        ('low', _('Faible')),
        ('medium', _('Moyen')),
        ('high', _('Élevé')),
    ]

    trend_type = models.CharField(max_length=20, choices=TREND_TYPE_CHOICES, verbose_name=_('Type de tendance'), help_text=_('Le type de tendance (émotion ou désinformation).'))
    trend_data = models.JSONField(verbose_name=_('Données de la tendance'), help_text=_('Les données de la tendance sous format JSON.'))
    alert_level = models.CharField(max_length=20, choices=ALERT_LEVEL_CHOICES, verbose_name=_('Niveau d\'alerte'), help_text=_('Le niveau d\'alerte de la tendance.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date et l\'heure de la création de la tendance.'))

    def __str__(self):
        return f'Tendance {self.get_trend_type_display()} - {self.get_alert_level_display()}'

    class Meta:
        verbose_name = _('Tendance de désinformation')
        verbose_name_plural = _('Tendances de désinformation')
        ordering = ['created_at']


class KnowledgeBase(models.Model):
    title = models.CharField(max_length=255, verbose_name=_('Titre'), help_text=_('Le titre de l\'article de la base de connaissances.'))
    content = models.TextField(verbose_name=_('Contenu'), help_text=_('Le contenu de l\'article de la base de connaissances.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date et l\'heure de la création de l\'article.'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Date de mise à jour'), help_text=_('La date et l\'heure de la dernière mise à jour de l\'article.'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Base de connaissances')
        verbose_name_plural = _('Bases de connaissances')
        ordering = ['created_at']


class Conversation(models.Model):
    STATUS_CHOICES = [
        ('active', _('Active')),
        ('ended', _('Terminé')),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conversations', verbose_name=_('Utilisateur'), help_text=_('L\'utilisateur impliqué dans la conversation.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date et l\'heure de création de la conversation.'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name=_('Statut'), help_text=_('Le statut de la conversation.'))
    is_archived = models.BooleanField(default=False, verbose_name=_('Archivée'), help_text=_('Indique si cette conversation est archivée.'))

    def __str__(self):
        return f'Conversation de {self.user} ({self.get_status_display()})'

    class Meta:
        verbose_name = _('Conversation')
        verbose_name_plural = _('Conversations')
        ordering = ['created_at']


class Message(models.Model):
    MESSAGE_TYPE_CHOICES = [
        ('text', _('Texte')),
        ('image', _('Image')),
        ('video', _('Vidéo')),
        ('audio', _('Son')),
        ('pdf', _('PDF')),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Conversation'), help_text=_('La conversation à laquelle ce message appartient.'))
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages', verbose_name=_('Utilisateur'), help_text=_('L\'utilisateur ayant envoyé ce message.'))
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, verbose_name=_('Type de message'), help_text=_('Le type de contenu du message.'))
    content = models.TextField(verbose_name=_('Contenu du message'), help_text=_('Le contenu du message.'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Date de création'), help_text=_('La date et l\'heure de création du message.'))

    def __str__(self):
        return f'Message de {self.user} dans la conversation {self.conversation.id}'

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['created_at']  # Permet de trier les messages par date de création.


class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', '👍'),
        ('dislike', '👎'),
        ('heart', '❤️'),
        ('lol', '😂'),
        ('wow', '😮'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reaction = models.CharField(choices=REACTION_CHOICES, max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Réaction de {self.user} au message {self.message.id}'


class TaskRecord(models.Model):
    task_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(  # <- NOUVEAU
        'CustomUser',  # ou settings.AUTH_USER_MODEL si CustomUser étend User
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks',
        verbose_name=_('Utilisateur'),
        help_text=_('L\'utilisateur ayant déclenché cette tâche.')
    )
    input_text = models.TextField()
    status = models.CharField(max_length=50, default='pending')  # pending / done / failure
    result = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Tâche {self.task_id} - {self.status}'

