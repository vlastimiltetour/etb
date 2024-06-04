from .base import *

# run from terminal
"""
export DJANGO_SETTINGS_MODULE=efir.settings.local
set DJANGO_SETTINGS_MODULE=efir.settings.local
python3 manage.py runserver 0.0.0.0:8000
ifconfig | grep "inet"
"""
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

ALLOWED_HOSTS = ["*", "localhost", "192.168.1.54"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


API_BASE_URL = os.getenv("API_BASE_URL")
ACCESS_TOKEN_URL = os.getenv("ACCESS_TOKEN_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE")
