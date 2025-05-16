import os
import sys
import django
import random
from faker import Faker

# Ajoutez le chemin du projet à PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from accounts.models import User, Notification, SupportTicket
from terranova.models import CustomUser, Dechet, PointCollecte, Evenement, Statistique, Recompense, Resource, News

# Configuration de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kabod.settings')
django.setup()

fake = Faker()

def create_fake_users(n=100):
    for _ in range(n):
        user = User.objects.create_user(
            username=fake.user_name(),
            email=fake.email(),
            password='pass123',
            phone=fake.phone_number(),
            email_verified=fake.boolean(),
            email_validation_token=fake.uuid4()
        )
        custom_user = CustomUser.objects.create(
            user_associated=user,
            points=random.randint(0, 100),
            role=random.choice(['utilisateur', 'administrateur', 'éco-influenceur', 'partenaire', 'municipalité'])
        )
        print(f'Utilisateur créé: {user.username}')

def create_fake_notifications(n=100):
    users = User.objects.all()
    for _ in range(n):
        Notification.objects.create(
            user=random.choice(users),
            message=fake.sentence(),
            is_read=fake.boolean()
        )
        print('Notification créée')

def create_fake_support_tickets(n=100):
    users = User.objects.all()
    for _ in range(n):
        SupportTicket.objects.create(
            user=random.choice(users),
            subject=fake.sentence(),
            message=fake.text(),
            is_resolved=fake.boolean()
        )
        print('Ticket de support créé')

def create_fake_dechets(n=100):
    users = CustomUser.objects.all()
    for _ in range(n):
        Dechet.objects.create(
            utilisateur=random.choice(users),
            photo=fake.image_url(),
            description=fake.text(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            statut=random.choice(['signalé', 'en_cours', 'traité'])
        )
        print('Déchet créé')

def create_fake_points_collecte(n=100):
    for _ in range(n):
        PointCollecte.objects.create(
            nom=fake.company(),
            latitude=random.uniform(-90, 90),
            longitude=random.uniform(-180, 180),
            niveau_remplissage=random.randint(0, 100),
            type=random.choice(['bac', 'centre'])
        )
        print('Point de collecte créé')

def create_fake_evenements(n=100):
    users = CustomUser.objects.all()
    for _ in range(n):
        Evenement.objects.create(
            utilisateur=random.choice(users),
            titre=fake.sentence(),
            description=fake.text(),
            date=fake.date_time_this_year(),
            lieu=fake.city()
        )
        print('Événement créé')

def create_fake_statistiques(n=100):
    users = CustomUser.objects.all()
    for user in users:
        Statistique.objects.create(
            utilisateur=user,
            dechets_signalés=random.randint(0, 100),
            dechets_recyclés=random.randint(0, 100)
        )
        print(f'Statistiques créées pour {user.username}')

def create_fake_recompenses(n=100):
    for _ in range(n):
        Recompense.objects.create(
            nom=fake.word(),
            description=fake.text(),
            points=random.randint(10, 100)
        )
        print('Récompense créée')

def create_fake_resources(n=100):
    for _ in range(n):
        Resource.objects.create(
            title=fake.sentence(),
            description=fake.text(),
            file=fake.file_path(depth=3, category='data')  # Simule un fichier
        )
        print('Ressource créée')

def create_fake_news(n=100):
    users = User.objects.all()
    for _ in range(n):
        News.objects.create(
            title=fake.sentence(),
            content=fake.text(),
            auteur=random.choice(users)
        )
        print('Actualité créée')

#if __name__ == "__main__":
print('on crée les fake datas !')
#create_fake_users(100)
create_fake_notifications(10)
create_fake_support_tickets(6)
create_fake_dechets(10)
create_fake_points_collecte(10)
create_fake_evenements(10)
create_fake_statistiques(10)
create_fake_recompenses(10)
create_fake_resources(50)
create_fake_news(50)