import os
import socket
import environ
from pathlib import Path

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, "django-insecure-kd(_c1v+$krer)303$3xbmhpg&tp^c*2w-te#mbtuvsm12-r5d"),
    REDIS_URL=(str, "redis://localhost:6379/0"),
    USE_CELERY_FALLBACK=(bool, False),
)

environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = ["*"]

# Applications
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",

    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",

    "accounts",
    "bomalokuta",
    "vax",
]

SITE_ID = 1
AUTH_USER_MODEL = "accounts.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kabod.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kabod.wsgi.application"

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Auth
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Passwords
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Langues
LANGUAGES = [
    ('fr', 'Français'),
    ('en', 'English'),
    ('ln', 'Lingala'),
    ('sw', 'Swahili'),
    ('kg', 'Kikongo'),
    ('ts', 'Tshiluba'),
]

LANGUAGE_CODE = 'fr'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Statics
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_DIRS = [BASE_DIR / "staticfiles"]

# DRF & Throttle
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "user": "120/minute",
        "anon": "60/minute",
    }
}

# Celery fallback (dev/local sans Redis worker)
USE_CELERY_FALLBACK = env.bool("USE_CELERY_FALLBACK", default=False)

if USE_CELERY_FALLBACK:
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
else:
    CELERY_BROKER_URL = env("REDIS_URL")
    CELERY_RESULT_BACKEND = env("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'


# Fonction pour vérifier si Redis est accessible localement
def is_redis_available(host='localhost', port=6379):
    try:
        with socket.create_connection((host, port), timeout=1):
            return True
    except OSError:
        return False

# Choix dynamique : Redis ou fallback
REDIS_ACTIVE = is_redis_available()

if REDIS_ACTIVE and not env.bool("USE_CELERY_FALLBACK"):
    print("✅ Redis détecté. Celery sera utilisé.")
    CELERY_BROKER_URL = env("REDIS_URL")  # ex: redis://localhost:6379/0
    CELERY_RESULT_BACKEND = env("REDIS_URL")
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'
else:
    print("⚠️ Redis non disponible. Mode Celery fallback (local).")
    CELERY_TASK_ALWAYS_EAGER = True
    CELERY_TASK_EAGER_PROPAGATES = True
# Logs simples
LOGGING = {
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}

USE_CELERY_FALLBACK = os.environ.get("USE_CELERY_FALLBACK", "true") == "true"
CELERY_TASK_ALWAYS_EAGER = USE_CELERY_FALLBACK
CELERY_TASK_EAGER_PROPAGATES = USE_CELERY_FALLBACK

CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# settings.py
USE_CELERY_FALLBACK = not os.getenv("USE_CELERY", "false").lower() in ["1", "true", "yes"]
