# storage_backends.py

from storages.backends.s3boto3 import S3Boto3Storage
from storages.utils import safe_join


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "public-read"
    file_overwrite = False
    querystring_auth = True

    def _normalize_name(self, name):
        try:
            return safe_join(self.location, name)
        except ValueError:
            # Log the error or handle it according to your needs
            # For example, strip leading slashes and retry
            name = name.lstrip("/")
            return safe_join(self.location, name)


class MediaStorage(S3Boto3Storage):
    location = "media"
    file_overwrite = False
    default_acl = "public-read"
    querystring_auth = True
