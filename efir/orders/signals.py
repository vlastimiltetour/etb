import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.mail_confirmation import *
from orders.models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def send_email_when_order_completed(sender, instance, **kwargs):
    logger.info(f"======= Product {instance} has been updated")

    if instance.shipped:
        order_shipped(instance.id)
        logger.info(
            f"======= Product {instance} has been dispatched to transport service"
        )
