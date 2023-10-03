from django.db import models


class Inventory(models.Model):
    product = models.ForeignKey(
        "catalog.Product",
        related_name="inventory",
        on_delete=models.CASCADE,
    )  # one to one relationship, each product has one inventory record
    size = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "nový rozměr produktu"
        verbose_name_plural = "Inventář"
        indexes = [
            models.Index(fields=["product", "size"]),
        ]

    def __str__(self):
        return f"{self.product.name} - Size: {self.size}, Quantity: {self.quantity}"
