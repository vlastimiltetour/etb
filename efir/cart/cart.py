import uuid  # Import the UUID module
from decimal import Decimal

from django.conf import settings

from catalog.forms import *
from catalog.models import Product
from coupons.models import Coupon


class Cart:
    def __init__(self, request):  # initialize the cart
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

        # store applied coupon
        self.coupon_id = self.session.get("coupon_id")

    def __iter__(self):
        item_ids = self.cart.keys()
        items = []

        self.cart.copy()

        for item_id in item_ids:
            product_id = self.cart[item_id]["product_id"]
            product = Product.objects.get(id=product_id)  # Use product_id

            cart_item = self.cart[item_id]
            cart_item["product"] = product
            cart_item["price"] = Decimal(cart_item["price"])
            cart_item["total_price"] = cart_item["price"] * cart_item["quantity"]
            items.append(cart_item)

        return iter(items)

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())


    def add(
        self,
        product,
        quantity=1,
        obvod_prsa=0,
        obvod_hrudnik=0,
        obvod_boky=0,
        obvod_body=0,
        zpusob_vyroby=None,  # might be renamed to konfekcni
        poznamka=None,
        override=False,
    ):
        cart_item_id = str(uuid.uuid4())

        # Check if the product is already in the cart
        for existing_cart_item_id, cart_item in self.cart.items():
            if "product_id" in cart_item and cart_item["product_id"] == product.id:
                if override:
                    # If override is True, update the quantity directly
                    cart_item["quantity"] = quantity
                    self.save()
                    return

        # If the product is not in the cart or override is True, add it as a new item
        self.cart[cart_item_id] = {
            "product_id": product.id,  # Store the product_id
            "quantity": quantity,
            "price": str(product.price),
            "obvod_boky": str(obvod_boky),
            "obvod_prsa": str(obvod_prsa),
            "obvod_hrudnik": str(obvod_hrudnik),
            "obvod_body": str(obvod_body),
            "poznamka": str(poznamka),
            "zpusob_vyroby": str(zpusob_vyroby),
        }

        self.save()


    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = product.id  # Assuming product_id is an integer field

        for item_id, cart_item in self.cart.items():
            """iterate over the dictionary, self.cart.items()
            is not a dictionary or a list by itself; it's actually
            an iterable view object in Python. It provides a way to access
            key-value pairs from a dictionary, similar to how you would iterate over items in a list.
            The key-value pairs are represented as tuples."""

            if "product_id" in cart_item and cart_item["product_id"] == product_id:
                del self.cart[item_id]
                self.save()
                break  # Exit the loop after removing the first matching item

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def get_shipping_price(self):
        # TODO this approach wouldn't work because I don't have the order ID yet.
        # Get the OrderForm data associated with the current cart, if it exists
        order_form_data = self.session.get("order_form_data")
        if order_form_data:
            country = order_form_data.get("order_country")
        else:
            country = "N/A"

            if country == "CZ":
                shipping_price = 79
            elif country == "SK":
                shipping_price = 89
            else:
                shipping_price = 89

        return shipping_price

    def get_total_price(self):
        product_discount = 0  # TODO subtrackt the discount from product price
        total_price = (
            sum(
                Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
            )
            + (self.get_shipping_price())
            - product_discount
        )
        return total_price

    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            discount = (self.coupon.discount / Decimal(100)) * self.get_total_price()

            return discount

        return Decimal(0)

    def get_total_price_after_discount(self):
        total_price = self.get_total_price()
        discount = self.get_discount()
        total_price_after_discount = total_price - discount

        return total_price_after_discount
