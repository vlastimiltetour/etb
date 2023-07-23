from django.conf import settings
from django.db import models

from catalog.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    COUNTRY_CHOICES = [("CZ", "Česko"), ("SK", "Slovensko"), ("ER", "EU")]

    country = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    shipping_type = (("Z", "Zásilkovna"), ("O", "Osobní odběr"))

    shipping = models.CharField(max_length=100, choices=shipping_type)
    address = models.CharField(max_length=250)

    stripe_id = models.CharField(max_length=250, blank=True)
    zasilkovna_id = models.CharField(max_length=250, blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Objednávky"
        verbose_name_plural = "Objednávky"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Order {self.id}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_stripe_url(self):
        if not self.stripe_id:
            return ""
        elif "_test_" in settings.STRIPE_SECRET_KEY:
            path = "/test/"
        else:
            path = "/"

        return f"https://dashboard.stripe.com{path}payments/{self.stripe_id}"

    def get_zasilkovna_url(self):
        pass


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.PositiveIntegerField(default=1)

    obvod_hrudnik = models.CharField(max_length=255, default="-", blank=True)
    obvod_prsa = models.CharField(max_length=255, default="-", blank=True)
    obvod_boky = models.CharField(max_length=255, default="-", blank=True)
    # obvod_body = models.CharField(max_length=255, default="-", blank=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
