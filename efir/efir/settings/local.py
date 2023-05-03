from .base import *

# run from terminal
"""
export DJANGO_SETTINGS_MODULE=efir.settings.local
set DJANGO_SETTINGS_MODULE=efir.settings.local
python3 manage.py runserver
"""
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

ALLOWED_HOSTS = ["*", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
