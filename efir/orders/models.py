from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

from catalog.models import Product


class Order(models.Model):
    etb_id = models.CharField(max_length=50, verbose_name="Efir ID")
    first_name = models.CharField(max_length=50, verbose_name="Jméno")
    last_name = models.CharField(max_length=50, verbose_name="Příjmení")
    birthday = models.DateField(verbose_name="Datum narození", null=True, blank=True)
    email = models.CharField(max_length=50, verbose_name="Email")
    number = models.CharField(max_length=20, verbose_name="Telefonní číslo")
    comments = models.TextField(blank=True, verbose_name="Komentáře")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Vytvořeno")
    updated = models.DateTimeField(auto_now=True, verbose_name="Aktualizováno")

    COUNTRY_CHOICES = [("CZ", "cz"), ("SK", "sk")]

    country = models.CharField(max_length=20, verbose_name="Země")
    shipping_type = (
        ("", "Vyberte si způsob dopravy"),
        ("P", "PPL"),
        ("Z", "Zásilkovna"),
        ("O", "Online"),
    )
    shipping = models.CharField(
        max_length=100,
        choices=shipping_type,
        verbose_name="Doprava",
        default="Zásilkovna",
    )
    shipping_price = models.DecimalField(
        decimal_places=0,
        max_digits=4,
        blank=True,
        default=Decimal("0"),
        verbose_name="Cena dopravy (CZK)",
    )
    address = models.CharField(max_length=250, verbose_name="Adresa", blank=False)
    city = models.CharField(max_length=250, verbose_name="City", blank=True, null=True)
    zipcode = models.CharField(max_length=250, verbose_name="Zipcode", blank=True, null=True)

    vendor_id = models.CharField(
        max_length=250,
        verbose_name="ID prodejce",
        blank=False,
    )
    discount = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        blank=True,
        default=Decimal("0"),
        verbose_name="Sleva (CZK)",
    )
    total_cost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        blank=True,
        default=Decimal("0.00"),
        verbose_name="Celková cena (CZK)",
    )

    stripe_id = models.CharField(max_length=250, blank=True, verbose_name="Stripe ID")
    zasilkovna_id = models.CharField(
        max_length=250, blank=True, verbose_name="Zásilkovna ID"
    )
    paid = models.BooleanField(default=False, verbose_name="Zaplaceno")
    shipped = models.BooleanField(default=False, verbose_name="Vyřízeno")
    newsletter_consent = models.BooleanField(
        default=False, verbose_name="Souhlas - newsletter", null=True, blank=True
    )
    author_comment = models.CharField(
        max_length=200, blank=True, verbose_name="ETB poznamka k objednavce"
    )
    discount_code = models.CharField(
        max_length=15, blank=True, default="-", verbose_name="Slevovy kod"
    )
    coupon_id = models.CharField(
        max_length=15, blank=True, default="-", verbose_name="ID certifikatu"
    )
    label = models.CharField(
        max_length=200, blank=True, null=True, verbose_name="Etiketa k doprave"
    )  # Or use FilePathField if you want to restrict to a certain directory

    class Meta:
        verbose_name = "Objednávky"
        verbose_name_plural = "Objednávky"
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return f"Objednávka {self.id}"

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

    def save(self, *args, **kwargs):
        # self.shipping_price = self.calculate_shipping_price()

        if "cart" in kwargs:
            cart = kwargs.pop("cart")
            cart.get_total_price_after_discount()

            self.shipping_price = cart.get_shipping_price()
            self.discount = cart.transfer_discount_to_orders()
            self.total_cost = cart.get_total_price_after_discount()

        if not self.etb_id:
            today_date = timezone.now().strftime("%y%m%d")
            today_order_count = Order.objects.filter(
                created__date=timezone.now().date()
            ).count()
            self.etb_id = f"{today_date}{today_order_count:02d}"

        """ vendor_id = kwargs.pop("vendor_id", None)
        if vendor_id:
            self.vendor_id = vendor_id

        print(f"model order printing vendor_id{vendor_id}")"""

        super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        decimal_places=0, max_digits=10, verbose_name="Cena za kus (CZK)"
    )
    total_price = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        verbose_name="Cena (CZK)",
        default=0,
    )
    surcharge = models.DecimalField(
        decimal_places=0,
        max_digits=10,
        verbose_name="Příplatek za šití na míru (CZK)",
        default=0,
    )
    quantity = models.PositiveIntegerField(default=1, verbose_name="Množství")

    zpusob_vyroby = models.CharField(max_length=50)
    velikost = models.CharField(
        max_length=50, null=True, blank=True, verbose_name="Individuální velikost"
    )
    kalhotky_velikost_set = models.CharField(max_length=50, null=True, blank=True)
    podprsenka_velikost_set = models.CharField(max_length=50, null=True, blank=True)
    pas_velikost_set = models.CharField(max_length=50, null=True, blank=True)

    poznamka = models.TextField(blank=True)
    slevovy_kod = models.CharField(
        max_length=20, default="-", verbose_name="Slevový kód"
    )
    hodnota_kuponu = models.CharField(
        max_length=20, default="-", verbose_name="Hodnota kuponu"
    )
    certificate_from = models.CharField(
        max_length=20, default="-", verbose_name="Od koho"
    )
    certificate_to = models.CharField(max_length=20, default="-", verbose_name="Komu")

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity
