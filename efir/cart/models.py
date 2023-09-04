# Create your models here.
from django.db import models

from catalog.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(
        Product, related_name="cart_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        decimal_places=2, max_digits=10, verbose_name="Cena za kus (CZK)"
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Množství")

    zpusob_vyroby = models.CharField(max_length=50)
    obvod_hrudnik = models.CharField(max_length=50, null=True, blank=True)
    obvod_prsa = models.CharField(max_length=50, null=True, blank=True)
    obvod_boky = models.CharField(max_length=50, null=True, blank=True)
    obvod_body = models.CharField(max_length=50, null=True, blank=True)
    poznamka = models.CharField(max_length=50)
