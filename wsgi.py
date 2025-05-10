import os
import sys

# Ajoutez le chemin vers votre projet Django à sys.path
path = '/home/bomalokuta/kabod'  # Remplacez ce chemin par le vôtre
if path not in sys.path:
    sys.path.append(path)

# Spécifiez le module de paramètres de votre projet
os.environ['DJANGO_SETTINGS_MODULE'] = 'kabod.settings'  # Remplacez 'monprojet' par le nom de votre projet

# Exécutez l'application Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()