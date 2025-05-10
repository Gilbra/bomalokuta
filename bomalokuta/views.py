from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Importez ceci pour gérer temporairement les requêtes POST sans token CSRF
# À utiliser avec EXTRÊME PRUDENCE en production !
from django.views.decorators.csrf import csrf_exempt
import json # Pour lire les données JSON envoyées dans le corps de la requête

from bomalokuta.models import *

from .utils import get_fake_news_detector

def home(request):
    try:
        # Récupère ou crée automatiquement un CustomUser lié à l'utilisateur connecté
        custom_user, _ = CustomUser.objects.get_or_create(user_associated=request.user)

        # Récupère toutes les soumissions de l'utilisateur via CustomUser
        submissions = Submission.objects.filter(user=custom_user)

        # Récupère un résumé des activités (par exemple, nombre de soumissions, score moyen)
        total_submissions = submissions.count()
        approved_submissions = submissions.filter(status='approved').count()
        pending_submissions = submissions.filter(status='pending').count()
        rejected_submissions = submissions.filter(status='rejected').count()
        average_score = submissions.aggregate(models.Avg('verification_score'))['verification_score__avg']
    except:
        # Si l'instance CustomUser n'existe pas, afficher un message d'erreur
        messages.error(request, "Vous n'êtes pas connecté, vos verifications ne seront pas enregistrées.")
    return render(request, 'bomalokuta/home.html', locals())

@login_required
def dashboard(request):
    try:
        # Récupère l'instance CustomUser associée à l'utilisateur connecté
        custom_user = CustomUser.objects.get(user_associated=request.user)

        # Récupère toutes les soumissions de l'utilisateur via CustomUser
        submissions = Submission.objects.filter(user=custom_user)

        # Récupère un résumé des activités (par exemple, nombre de soumissions, score moyen)
        total_submissions = submissions.count()
        approved_submissions = submissions.filter(status='approved').count()
        pending_submissions = submissions.filter(status='pending').count()
        rejected_submissions = submissions.filter(status='rejected').count()
        average_score = submissions.aggregate(models.Avg('verification_score'))['verification_score__avg']
    except CustomUser.DoesNotExist:
        # Si l'instance CustomUser n'existe pas, afficher un message d'erreur
        messages.error(request, "Vous n'êtes pas connecté, vos verifications ne seront pas enregistrées.")

    return render(request, 'bomalokuta/dashboard.html', locals())

@csrf_exempt # <-- Déactive la protection CSRF pour ce point de vue (temporaire/pour tests)
def analyze_text_view(request):
    """
    Reçoit une requête POST avec du texte à analyser et retourne un résultat (placeholder).
    """
    if request.method == 'POST':
        try:
            # Tente de lire le corps de la requête en JSON.
            # Les données envoyées (par le web, WhatsApp, SMS gateway) seront probablement JSON.
            data = json.loads(request.body.decode('utf-8'))
            text_to_analyze = data.get('text', None) # On s'attend à une clé 'text'

            if text_to_analyze:
                print(f"Texte reçu à analyser : {text_to_analyze}") # Log dans la console du serveur

                # --- LOGIQUE FUTURE PRINCIPALE ICI ---
                # Étape 4: Appeler le modèle IA avec text_to_analyze
                # Étape 5: Effectuer la recherche web avec text_to_analyze ou des termes dérivés
                # Étape 6: Combiner les résultats de l'IA et de la recherche web pour l'analyse finale
                # Déterminer si l'info est vraie/fausse et générer des commentaires/sources
                # --- FIN LOGIQUE FUTURE ---

                # Pour l'instant, on renvoie juste une confirmation
                response_data = {
                    'status': 'success',
                    'received_text': "Gilbra",
                    'message': "Gilbra",
                    'analysis_result': 'pending' # Placeholder
                }
                # On retourne une réponse JSON
                return JsonResponse(response_data, status=200)
            else:
                form = request.cleaned_data
                content = form['content']
                # Si le champ 'text' est manquant dans le JSON
                return JsonResponse({'status': 'error', 'message': 'Champ "text" manquant dans le corps de la requête. ','content':content}, status=400)

        except json.JSONDecodeError:
            # Si le corps de la requête n'est pas un JSON valide
            return JsonResponse({'status': 'error', 'message': 'Format de requête invalide (doit être JSON).'}, status=400)
        except Exception as e:
            # Pour capturer d'autres erreurs inattendues
            print(f"Erreur interne : {e}") # Log l'erreur
            return JsonResponse({'status': 'error', 'message': f'Une erreur interne est survenue : {str(e)}'}, status=500)
    else:
        # Si la méthode HTTP n'est pas POST
        return JsonResponse({'status': 'error', 'message': 'Seules les requêtes POST sont acceptées pour cette URL.'}, status=405)

@csrf_exempt
@login_required
def add_reaction(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_id = data['message_id']
            reaction_type = data['reaction']

            custom_user = CustomUser.objects.get(user_associated=request.user)
            message = Message.objects.get(id=message_id)

            # Crée ou met à jour la réaction
            Reaction.objects.update_or_create(
                user=custom_user,
                message=message,
                defaults={'reaction': reaction_type}
            )
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

