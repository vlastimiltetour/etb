"""
Django settings for efirthebrand project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os
from pathlib import Path

from django.core.mail import EmailMessage
from dotenv import load_dotenv

load_dotenv(".env")

DJANGO_SETTINGS_MODULE = "efir.settings.local"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")


#ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",  # anonymous sessions https://docs.djangoproject.com/en/4.1/topics/http/sessions/#module-django.contrib.sessions
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "catalog.apps.CatalogConfig",
    "orders.apps.OrdersConfig",
    "cart.apps.CartConfig",
    "django.contrib.humanize",
]


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "efir.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "cart.context_processors.cart",
                "catalog.context_processors.categories",
            ],
        },
    },
]

WSGI_APPLICATION = "efir.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# Maximum size of a file that can be uploaded, added to django settings + settings updated in nginx
DATA_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20 MB

# Maximum size of a request that can be parsed by Django
# Set it to a value larger than DATA_UPLOAD_MAX_MEMORY_SIZE
# to allow handling larger files
FILE_UPLOAD_MAX_MEMORY_SIZE = 20971520  # 20 MB


STATIC_URL = "static/"
STATIC_ROOT = (
    BASE_DIR / "static"
)  # this solves the issue of django.core.exceptions.ImproperlyConfigured: You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.


MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This is the key that is going to be used to store the cart in the user session.
CART_SESSION_ID = "cart"


# this is to make Django to write emails to the console
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Setting up email server FORPSI
# https://support.forpsi.com/kb/a3147/konfigurace-smtp-serveru.aspx
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.forpsi.com"
EMAIL_HOST_USER = "objednavky@efirthebrand.cz"
EMAIL_HOST_PASSWORD = ",4d?SAF9A>Ra@f"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "objednavky@efirthebrand.cz"
EMAIL_ENCRYPTION = "STARTTLS"

ASGI_APPLICATION = "web.asgi.application"
