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
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]["product"] = product

        for item in cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            yield item

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
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
                "obvod_boky": obvod_boky,
                "obvod_prsa": obvod_prsa,
                "obvod_hrudnik": obvod_hrudnik,
                "obvod_body": obvod_body,
                "poznamka": poznamka,
                "zpusob_vyroby": str(zpusob_vyroby),
            }

        if override:
            self.cart[product_id]["quantity"] = quantity
            self.cart[product_id]["obvod_boky"] = obvod_boky
            self.cart[product_id]["obvod_prsa"] = obvod_prsa
            self.cart[product_id]["obvod_hrudnik"] = obvod_hrudnik
            self.cart[product_id]["obvod_body"] = obvod_body
            self.cart[product_id]["zpusob_vyroby"] = str(zpusob_vyroby)

        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

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
            elif country == "EU":
                shipping_price = 0
            else:
                shipping_price = 0

        return shipping_price

    def get_total_price(self):
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        ) + (self.get_shipping_price())

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
