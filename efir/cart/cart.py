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
        self.country = self.session.get("cart_country")
        self.address = self.session.get("cart_address")
        self.vendor_id = self.session.get("cart_vendor")

    def __iter__(self):  # this is a view
        item_ids = self.cart.keys()
        items = []  # temporary data structure used to organize and prep cart data

        self.cart.copy()  # creating a copy to prevent changes to original cart data

        for item_id in item_ids:
            product_id = self.cart[item_id]["product_id"]

            try:
                product = Product.objects.get(id=product_id)  # Use product_id
            except Product.DoesNotExist:
                return self.clean_cart_session()

            cart_item = self.cart[item_id]
            cart_item["product"] = product
            cart_item["price"] = Decimal(cart_item["price"])
            # print("tohle je cart item surcharge type")
            # print(type(cart_item["quantity"]))
            cart_item["total_surcharge"] = cart_item["quantity"] * int(
                cart_item["surcharge"]
            )
            cart_item["discounted_price_cart"] = product.corrected_price
            cart_item["total_price"] = cart_item["price"] * cart_item["quantity"]

            items.append(cart_item)

        return iter(items)

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def add(
        self,
        product,
        quantity=1,
        velikost=0,
        kalhotky_velikost_set=0,
        podprsenka_velikost_set=0,
        pas_velikost_set=0,
        zpusob_vyroby=None,  # might be renamed to konfekcni
        poznamka=None,
        override=None,
    ):
        # Check if the product is already in the cart

        # Check if the product is already in the cart
        for cart_item_id, cart_item_value in self.cart.items():
            print(cart_item_value)

        """for cart_item_id, cart_item_value in self.cart.items():
            if cart_item_value["product_id"] == product.id:
                # Product already in cart, update the quantity
                print(f"Updating quantity of product {product.id} to {quantity}")
                cart_item_value["quantity"] += quantity
                self.save()
                return"""

        # Generate a new cart item_id
        cart_item_id = str(uuid.uuid4())

        surcharge = int(0)
        if zpusob_vyroby == "Na Míru":
            surcharge = int(product.price * Decimal(str(0.3)))

        # If the item_id is already in the cart, allow adjusting the quantity
        if cart_item_id in self.cart:
            self.cart[cart_item_id]["quantity"] += quantity
        else:
            # Add the product as a new item
            self.cart[cart_item_id] = {
                "item_id": cart_item_id,
                "product_id": product.id,
                "quantity": quantity,
                "price": str(product.price),
                "surcharge": str(surcharge),
                "velikost": str(velikost),
                "kalhotky_velikost_set": str(kalhotky_velikost_set),
                "podprsenka_velikost_set": str(podprsenka_velikost_set),
                "pas_velikost_set": str(pas_velikost_set),
                "poznamka": str(poznamka),
                "zpusob_vyroby": str(zpusob_vyroby),
                "override": override,
            }

        self.save()
        # Generate a new cart item_id
        cart_item_id = str(uuid.uuid4())

    def save(self):
        self.session.modified = True

    def update_quantity(self, item_id, new_quantity):
        if item_id in self.cart:
            self.cart[item_id]["quantity"] = new_quantity
            self.save()

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
        # Get the country from the cart data
        country = self.country

        if country == "cz":
            shipping_price = 89
        elif country == "sk":
            shipping_price = 99
        else:
            shipping_price = 0

        return shipping_price

    def get_address(self):
        address = self.address

        if address is not None:
            return address

        return "Nevyplněno"

    def get_country(self):
        country = self.country

        if country is not None:
            return country

        return "Nevyplněno"

    def get_vendor(self):
        vendor = self.vendor_id

        if vendor is not None:
            return vendor

        return "Nevyplněno"

    def clean_cart_session(self):
        # Clean up the cart session
        del self.session[settings.CART_SESSION_ID]

        try:
            del self.session["coupon_id"]
            del self.session["cart_country"]
            del self.session["cart_address"]
            del self.session["cart_vendor"]
        except KeyError:
            print("all good")

        self.save()

    def get_total_surcharge(self):
        surcharge = sum(
            int(item["surcharge"]) * item["quantity"] for item in self.cart.values()
        )

        return int(surcharge)

    def get_total_price(self):
        # product_discount = product.corrected_price()
        # print("this is product corrected price:", product_discount)
        product_discount = 0
        # access to the Product instance within the Cart class
        for item in self.cart.values():
            product_id = item["product_id"]
            quantity = item["quantity"]
            item["surcharge"]

            try:
                product = Product.objects.get(id=product_id)
                product_discount += (
                    product.cart_discounted_price() * quantity
                )  # Assuming corrected_price() is a method of the Product model
                print("------")
                print("this is product discount:", product_discount)
                print("------")

            except Product.DoesNotExist:
                pass

        total_price = (
            sum((item["price"]) * item["quantity"] for item in self.cart.values())
            + (self.get_shipping_price() + self.get_total_surcharge())
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
            discount = self.coupon.discount_value

            return discount

        return Decimal(0)

    def get_discount_percentage(self):
        if self.coupon:
            discount = self.coupon.discount_value

            return discount * 100

        return Decimal(0)

    def get_discount_threshold(self):
        if self.coupon:
            threshold = self.coupon.discount_threshold

            return threshold

        return None

    def get_discount_type(self):
        if self.coupon:
            type = self.coupon.discount_type

            return type

        return None

    def get_total_price_after_discount(self):
        total_price = self.get_total_price()
        discount = self.get_discount()

        if self.get_discount_threshold():
            if total_price >= self.get_discount_threshold():
                if self.get_discount_type() == "Procento":
                    total_price_after_discount = total_price * (1 - discount)
                    return total_price_after_discount
                elif self.get_discount_type() == "Částka":
                    total_price_after_discount = total_price - discount
                    return total_price_after_discount

            else:
                return f"Nelze aplikovat slevu, minimální nákup {self.get_discount_threshold()}"

        total_price_after_discount = self.get_total_price()

        return total_price_after_discount
    
    def transfer_discount_to_orders(self):
        return self.get_total_price_after_discount() - self.get_total_price()
