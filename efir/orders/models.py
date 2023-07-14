from django.db import models

from catalog.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    number = models.CharField(max_length=20)
    comments = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    shipping_type = (("Z", "Zásilkovna"), ("O", "Osobní odběr"))

    shipping = models.CharField(max_length=100, choices=shipping_type)
    address = models.CharField(max_length=250)

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
