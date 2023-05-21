from decimal import Decimal

from django.conf import settings

from catalog.models import Product
from catalog.forms import *

class Cart:
    def __init__(self, request):  # initialize the cart
        self.session = request.session
        # which represents the current user's session, requesting the key to make it accessible to other methods of Cart class
        cart = self.session.get(
            settings.CART_SESSION_ID
        )  # try to get the key from session / cart from the current session
        if (
            not cart
        ):  # save an empty cart in the session, if no cart is yet present, create the cart
            cart = self.session[settings.CART_SESSION_ID] = {}  # initiate the cart

        self.cart = cart  # redefine cart as an instance of the Cart class

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])  # converting to decimals
            item["total_price"] = item["price"] * item["quantity"]
            item["obvod_prsa"] = item.get("obvod_prsa")
            item["obvod_hrudnik"] = item.get("obvod_hrudnik")
            yield item

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity, obvod_prsa, obvod_hrudnik, override_quantity=False):
        product_id = str(product.id)  # string because it's a dictionary

        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, 
                                     "price": str(product.price),
                                     "obvod_prsa": str(obvod_prsa),
                                     "obvod_hrudnik": str(obvod_hrudnik),
                                     }

        if override_quantity:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True  # saving the session

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )
