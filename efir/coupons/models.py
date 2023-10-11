from django.db import models


class Coupon(models.Model):
    code = models.CharField(max_length=10, unique=True, help_text="Váš slevový kód:")
    valid_from = models.DateField()
    valid_to = models.DateField()
    """discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Sleva v procentech 0 az 100",
    )"""
    discount = models.DecimalField(max_digits=10, decimal_places=0)
    active = models.BooleanField(verbose_name="Aktivní")
    redeemed = models.BooleanField(default=False, verbose_name="Uplatněno")

    def __str__(self):
        return self.code
