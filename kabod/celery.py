import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kabod.settings')

app = Celery('kabod')

# Production
app.conf.broker_url = os.getenv("REDIS_URL")
app.conf.result_backend = os.getenv("REDIS_URL")

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
