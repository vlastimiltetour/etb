# In your catalog/signals.py file
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from cart.cart import \
    Cart  # Adjust this import based on your actual cart model
from catalog.models import Product  # Import your Product model


@receiver(pre_delete, sender=Product)
def clear_cart_on_product_delete(sender, instance, **kwargs):
    """
    Remove the product from the cart and then clear the cart when a product is deleted.
    """
    cart = Cart()
    cart.remove(instance)
    cart.clear()
