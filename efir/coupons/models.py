from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Váš slevový kód:")
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Sleva v procentech 0 az 100",
    )
    active = models.BooleanField()

    def __str__(self):
        return self.code
