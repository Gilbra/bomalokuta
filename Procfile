# Procfile
web: gunicorn kabod.wsgi --log-file -
worker: celery -A kabod worker --loglevel=info