import os

from .base import *

DEBUG = bool(os.getenv("DEBUG") == "True")


# Spaces settings
# https://stackoverflow.com/questions/76940089/signaturedoesnotmatch-digitalocean-spaces-boto3-django-storages-django
AWS_ACCESS_KEY_ID = str(os.getenv("AWS_ACCESS_KEY_ID"))
AWS_SECRET_ACCESS_KEY = str(os.getenv("AWS_SECRET_ACCESS_KEY"))
AWS_STORAGE_BUCKET_NAME = "etb"
AWS_DEFAULT_ACL = "public-read"
AWS_S3_ENDPOINT_URL = f"https://{AWS_STORAGE_BUCKET_NAME}.fra1.digitaloceanspaces.com"

AWS_S3_REGION_NAME = "fra1"

AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read",  # THIS LINE IS OPTIONAL
}

# static settings
# AWS_LOCATION = 'static'


# Static files settings: this works
STATIC_URL = f"https://{AWS_S3_ENDPOINT_URL}/static/"
STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Optional: Set S3 object parameters
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read",
}

# Public media files
AWS_PUBLIC_MEDIA_LOCATION = "media"
DEFAULT_FILE_STORAGE = "efir.settings.storage_backends.MediaStorage"
MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_PUBLIC_MEDIA_LOCATION}/"

# Optional: Set S3 object parameters (again, if needed)
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read",
}


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

API_BASE_URL = os.getenv("API_BASE_URL")
ACCESS_TOKEN_URL = os.getenv("ACCESS_TOKEN_URL")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = os.getenv("SCOPE")


# settings.py
