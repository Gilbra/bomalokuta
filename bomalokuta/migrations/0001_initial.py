# Generated by Django 5.2 on 2025-04-05 13:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DisinformationTrend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trend_type', models.CharField(choices=[('emotion', 'Émotion'), ('disinformation', 'Désinformation')], help_text='Le type de tendance (émotion ou désinformation).', max_length=20, verbose_name='Type de tendance')),
                ('trend_data', models.JSONField(help_text='Les données de la tendance sous format JSON.', verbose_name='Données de la tendance')),
                ('alert_level', models.CharField(choices=[('low', 'Faible'), ('medium', 'Moyen'), ('high', 'Élevé')], help_text="Le niveau d'alerte de la tendance.", max_length=20, verbose_name="Niveau d'alerte")),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la création de la tendance.", verbose_name='Date de création')),
            ],
            options={
                'verbose_name': 'Tendance de désinformation',
                'verbose_name_plural': 'Tendances de désinformation',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='KnowledgeBase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Le titre de l'article de la base de connaissances.", max_length=255, verbose_name='Titre')),
                ('content', models.TextField(help_text="Le contenu de l'article de la base de connaissances.", verbose_name='Contenu')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la création de l'article.", verbose_name='Date de création')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text="La date et l'heure de la dernière mise à jour de l'article.", verbose_name='Date de mise à jour')),
            ],
            options={
                'verbose_name': 'Base de connaissances',
                'verbose_name_plural': 'Bases de connaissances',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('user', 'Utilisateur'), ('journalist', 'Journaliste'), ('fact_checker', 'Vérificateur'), ('admin', 'Administrateur')], default='user', help_text='Le rôle de cet utilisateur.', max_length=20, verbose_name='Rôle')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='La date de création de ce profil.', verbose_name='Date de création')),
                ('is_active', models.BooleanField(default=True, help_text='Indique si cet utilisateur est actif ou non.', verbose_name='Actif')),
                ('profile_picture', models.ImageField(blank=True, help_text="L'image de profil de l'utilisateur.", null=True, upload_to='user_profiles/', verbose_name='Image de profil')),
                ('user_associated', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='custom_user', to=settings.AUTH_USER_MODEL, verbose_name='Utilisateur associé')),
            ],
            options={
                'verbose_name': 'Utilisateur personnalisé',
                'verbose_name_plural': 'Utilisateurs personnalisés',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de création de la conversation.", verbose_name='Date de création')),
                ('status', models.CharField(choices=[('active', 'Active'), ('ended', 'Terminé')], default='active', help_text='Le statut de la conversation.', max_length=20, verbose_name='Statut')),
                ('is_archived', models.BooleanField(default=False, help_text='Indique si cette conversation est archivée.', verbose_name='Archivée')),
                ('user', models.ForeignKey(help_text="L'utilisateur impliqué dans la conversation.", on_delete=django.db.models.deletion.CASCADE, related_name='conversations', to='bomalokuta.customuser', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Conversation',
                'verbose_name_plural': 'Conversations',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(choices=[('text', 'Texte'), ('image', 'Image'), ('video', 'Vidéo'), ('audio', 'Son'), ('pdf', 'PDF')], help_text='Le type de contenu du message.', max_length=20, verbose_name='Type de message')),
                ('content', models.TextField(help_text='Le contenu du message.', verbose_name='Contenu du message')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de création du message.", verbose_name='Date de création')),
                ('conversation', models.ForeignKey(help_text='La conversation à laquelle ce message appartient.', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='bomalokuta.conversation', verbose_name='Conversation')),
                ('user', models.ForeignKey(help_text="L'utilisateur ayant envoyé ce message.", on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='bomalokuta.customuser', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(help_text='Label à vérifier pour cette soumission.', max_length=255, verbose_name='Label de vérification')),
                ('submission_date', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la soumission.", verbose_name='Date de soumission')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text="La date et l'heure de la dernière mise à jour de la soumission.", verbose_name='Date de mise à jour')),
                ('verification_score', models.FloatField(blank=True, help_text='Le score de vérification de ce contenu.', null=True, verbose_name='Score de vérification')),
                ('status', models.CharField(default='pending', help_text='Le statut de la soumission (En attente, Validée, Rejetée).', max_length=20, verbose_name='Statut')),
                ('priority', models.CharField(choices=[('low', 'Faible'), ('medium', 'Moyenne'), ('high', 'Haute')], default='medium', help_text='La priorité de la soumission.', max_length=20, verbose_name='Priorité')),
                ('user', models.ForeignKey(help_text="L'utilisateur ayant soumis ce contenu.", on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='bomalokuta.customuser', verbose_name='Utilisateur')),
            ],
            options={
                'verbose_name': 'Soumission',
                'verbose_name_plural': 'Soumissions',
                'ordering': ['submission_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(help_text='Le contenu du commentaire.', verbose_name='Commentaire')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure du commentaire.", verbose_name='Date du commentaire')),
                ('user', models.ForeignKey(help_text="L'utilisateur ayant rédigé ce commentaire.", on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bomalokuta.customuser', verbose_name='Utilisateur')),
                ('submission', models.ForeignKey(help_text='La soumission associée à ce commentaire.', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='bomalokuta.submission', verbose_name='Soumission')),
            ],
            options={
                'verbose_name': 'Commentaire',
                'verbose_name_plural': 'Commentaires',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='SubmissionElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_type', models.CharField(choices=[('article', 'Article'), ('video', 'Vidéo'), ('message', 'Message'), ('image', 'Image'), ('audio', 'Son'), ('pdf', 'PDF')], help_text='Le type de contenu (Article, Vidéo, etc.).', max_length=20, verbose_name='Type de contenu')),
                ('content', models.TextField(help_text="Le contenu de l'élément (texte, lien, etc.).", verbose_name='Contenu')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la création de cet élément.", verbose_name='Date de création')),
                ('order', models.PositiveIntegerField(default=0, help_text="Détermine l'ordre d'affichage des éléments dans la soumission.", verbose_name="Ordre d'affichage")),
                ('submission', models.ForeignKey(help_text='La soumission à laquelle cet élément appartient.', on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='bomalokuta.submission', verbose_name='Soumission')),
            ],
            options={
                'verbose_name': 'Élément de soumission',
                'verbose_name_plural': 'Éléments de soumission',
                'ordering': ['order', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='TextAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('analysis_result', models.JSONField(help_text="Les résultats de l'analyse de texte sous format JSON.", verbose_name="Résultats de l'analyse")),
                ('emotion_results', models.JSONField(help_text="Les résultats de l'analyse des émotions sous format JSON.", verbose_name='Résultats des émotions')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la création de l'analyse.", verbose_name="Date d'analyse")),
                ('submission', models.OneToOneField(help_text='La soumission analysée.', on_delete=django.db.models.deletion.CASCADE, related_name='text_analysis', to='bomalokuta.submission', verbose_name='Soumission')),
            ],
            options={
                'verbose_name': 'Analyse de texte',
                'verbose_name_plural': 'Analyses de texte',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verification_result', models.JSONField(help_text='Le résultat détaillé de la vérification sous format JSON.', verbose_name='Résultat de la vérification')),
                ('comments', models.TextField(blank=True, help_text="Des commentaires supplémentaires de l'expert concernant la vérification.", null=True, verbose_name='Commentaires')),
                ('verification_date', models.DateTimeField(auto_now_add=True, help_text="La date et l'heure de la vérification.", verbose_name='Date de vérification')),
                ('is_verified', models.BooleanField(default=False, help_text='Indique si cette soumission a été vérifiée.', verbose_name='Vérifié')),
                ('next_verification_date', models.DateTimeField(blank=True, help_text='La date prévue pour la prochaine vérification.', null=True, verbose_name='Prochaine date de vérification')),
                ('expert', models.ForeignKey(help_text="L'expert ayant effectué la vérification.", on_delete=django.db.models.deletion.CASCADE, related_name='verifications_given', to='bomalokuta.customuser', verbose_name='Expert')),
                ('submission', models.ForeignKey(help_text='La soumission à vérifier.', on_delete=django.db.models.deletion.CASCADE, related_name='verifications', to='bomalokuta.submission', verbose_name='Soumission')),
            ],
            options={
                'verbose_name': 'Vérification',
                'verbose_name_plural': 'Vérifications',
                'ordering': ['verification_date'],
            },
        ),
    ]
