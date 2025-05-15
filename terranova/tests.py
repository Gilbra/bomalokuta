from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser, Dechet, PointCollecte, Evenement, Statistique, Recompense

class CustomUserTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')

    def test_create_user(self):
        url = reverse('customuser-list')
        data = {
            'user_associated': self.user.id,
            'points': 10,
            'role': 'utilisateur'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class DechetTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.dechet = Dechet.objects.create(utilisateur=self.user, description='Déchet test', latitude=45.0, longitude=5.0)

    def test_dechet_creation(self):
        url = reverse('dechet-list')
        data = {
            'utilisateur': self.user.id,
            'description': 'Nouveau déchet',
            'latitude': 45.0,
            'longitude': 5.0,
            'photo': '',  # Ajoutez un fichier d'image si nécessaire
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class PointCollecteTests(APITestCase):
    def test_point_collecte_creation(self):
        url = reverse('pointcollecte-list')
        data = {
            'nom': 'Bac à déchets',
            'latitude': 45.0,
            'longitude': 5.0,
            'niveau_remplissage': 50,
            'type': 'bac'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EvenementTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')

    def test_evenement_creation(self):
        url = reverse('evenement-list')
        data = {
            'utilisateur': self.user.id,
            'titre': 'Événement test',
            'description': 'Description de l\'événement',
            'date': '2025-05-15T10:00:00Z',
            'lieu': 'Lieu de l\'événement'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class RecompenseTests(APITestCase):
    def test_recompense_creation(self):
        url = reverse('recompense-list')
        data = {
            'nom': 'Recompense test',
            'description': 'Description de la recompense',
            'points': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class StatistiqueTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.statistique = Statistique.objects.create(utilisateur=self.user)

    def test_statistique_creation(self):
        url = reverse('statistique-list')
        data = {
            'utilisateur': self.user.id,
            'dechets_signalés': 5,
            'dechets_recyclés': 3
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)