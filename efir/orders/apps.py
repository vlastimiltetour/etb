import logging

from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"

    def ready(self):
        from . import signals  # noqa: F401

        logging.getLogger("django").info("Catalog signals imported")
