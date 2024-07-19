import logging

from django.conf import settings
from django.contrib.sessions.models import Session
from django.db.models.signals import post_delete
from django.dispatch import receiver

from catalog.models import Product

logger = logging.getLogger(__name__)


@receiver(post_delete, sender=Product)
def clear_cart_on_product_delete(sender, instance, **kwargs):
    """
    Remove the product from all carts when a product is deleted.
    """
    logger.info(f"======= Product {instance.name} deleted")

    """ #his would be to delete the product from the cart
    sessions = Session.objects.all()
    for session in sessions:
        session_data = session.get_decoded()
        cart_data = session_data.get(settings.CART_SESSION_ID, {})
        if str(instance.id) in cart_data:
            del cart_data[str(instance.id)]
            session_data[settings.CART_SESSION_ID] = cart_data
            session.session_data = Session.objects.encode(session_data)
            session.save()
            logger.info(f"Product {instance.name} removed from Cart in session {session.session_key}")
"""

    # this is to delete the whole session
    sessions = Session.objects.all()
    for session in sessions:
        session_data = session.get_decoded()
        if settings.CART_SESSION_ID in session_data:
            del session_data[settings.CART_SESSION_ID]
            session.session_data = Session.objects.encode(session_data)
            session.save()
            logger.info(f"Cart cleared in session {session.session_key}")

    logger.info(f"Completed removing product {instance.name} from all carts")
