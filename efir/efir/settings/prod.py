import os
from .base import *



DEBUG = bool(os.getenv("DEBUG") == "True")

ADMINS = [
    ("Val", "v.tetour@gmail.com"),
]

ALLOWED_HOSTS = [
    "efirthebrand.cz",
    "www.efirthebrand.cz",
    "46.101.174.92",
    "localhost",
    "127.0.0.1",
    "[::1]",
]
# https://kinsta.com/knowledgebase/edit-mac-hosts-file/


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": 5432,
    }
}


# broker settings from: https://kyria.github.io/LazyBlacksmith/getting_started/docker/
CELERY_BROKER_URL = str(os.getenv("CELERY_BROKER_URL"))
CELERY_RESULT_BACKEND = str(os.getenv("CELERY_RESULT_BACKEND"))

# Security
CSRF_COOKIE_SECURE = bool(os.getenv("CSRF_COOKIE_SECURE") == "True")
SESSION_COOKIE_SECURE = bool(os.getenv("SESSION_COOKIE_SECURE") == "True")
SECURE_SSL_REDIRECT = bool(os.getenv("SECURE_SSL_REDIRECT") == "True")
