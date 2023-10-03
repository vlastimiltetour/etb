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

DJANGO_SETTINGS_MODULE = "efir.settings.local"

import logging

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("Loading local Env Module")
    import dotenv

    dotenv.read_dotenv()
    environment = "local"
except AttributeError:
    from dotenv import load_dotenv

    load_dotenv(".env")
    logging.info("Exception raised, means Production Env should be executed.")
    logging.info("Loading Production Env Module")
finally:
    logging.info("The whole cycle finished")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG")


# ALLOWED_HOSTS = []


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
    "payments.apps.PaymentsConfig",
    "orders.apps.OrdersConfig",
    "cart.apps.CartConfig",
    "django.contrib.humanize",
    "coupons.apps.CouponsConfig",
    "stripepayment.apps.StripepaymentConfig",
    "newsletter.apps.NewsletterConfig",
    "inventory.apps.InventoryConfig",
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
        "DIRS": ["templates"],
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

# generating pdf
STATIC_ROOT = BASE_DIR / "static"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This is the key that is going to be used to store the cart in the user session.
CART_SESSION_ID = "cart"
ORDER_SESSION_ID = "order"


# this is to make Django to write emails to the console
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Setting up email server FORPSI
# https://support.forpsi.com/kb/a3147/konfigurace-smtp-serveru.aspx
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")
EMAIL_ENCRYPTION = os.getenv("EMAIL_ENCRYPTION")

ASGI_APPLICATION = "web.asgi.application"

# stripe credentials
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
STRIPE_API_VERSION = os.getenv("STRIPE_API_VERSION")


# zasilkovna
ZASILKOVNA_API_KEY = os.getenv("ZASILKOVNA_API_KEY")
ZASILKOVNA_SECRET = os.getenv("ZASILKOVNA_SECRET")
