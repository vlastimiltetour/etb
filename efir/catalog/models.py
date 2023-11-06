from django.core.validators import EmailValidator
from django.db import models
from django.urls import reverse  # this is when calling an address by name
from PIL import Image, ImageOps


# Create your models here.
class Product(models.Model):
    # Product specaifics

    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.CASCADE,
    )  # one to many relationship, a product belongs to one category and a category contains multiple products
    # So if you have a Category instance cat, you can access all the related Product instances by calling
    # cat.products.all()

    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    short_description = models.TextField(max_length=50, blank=True)
    long_description = models.TextField(blank=True)

    # Time Specifics
    new = models.BooleanField(default=False)
    limited = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    bestseller = models.BooleanField(default=False)
    headliner = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=2, decimal_places=0, blank=True, null=True
    )

    # velikost = models.ManyToManyField(Inventory, blank=True, verbose_name="velikost")

    zpusob_vyroby = models.ManyToManyField(
        "ZpusobVyroby",
        blank=False,
        default="Skladem",
        verbose_name="Druh kolekce",
    )

    poznamka = models.TextField(blank=True)

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def get_available_sizes(self):
        # Retrieve the available sizes for this product from the associated inventory
        sizes = self.inventory.values_list("size", flat=True).distinct()
        return list(sizes)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.id, self.slug])


class Category(models.Model):
    CATEGORY_CHOICES = [
        ("Celé sety", "Celé sety"),
        ("Podprsenky", "Podprsenky"),
        ("Kalhotky", "Kalhotky"),
        ("Podvazkové pasy", "Podvazkové pasy"),
        ("Body", "Body"),
        ("Doplňky", "Doplňky"),
        ("Dárkové certifikáty", "Dárkové certifikáty"),
    ]
    name = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    slug = models.SlugField(
        max_length=255, null=False, unique=True
    )  # unique creates an index

    # additional information about Category model
    class Meta:
        verbose_name = "Kategorie"
        verbose_name_plural = "Kategorie"
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=["name"]
            ),  # this piece of code improves query performance
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(
        self,
    ):
        return reverse("catalog:product_list_by_category", args=[self.slug])


class ZpusobVyroby(models.Model):
    ZPUSOB_VYROBY_CHOICES = [
        ("Skladem", "Skladem"),
        ("Na Míru", "Na Míru"),
        ("-", "-"),
    ]

    size = models.CharField(
        max_length=20,
        choices=ZPUSOB_VYROBY_CHOICES,
        blank=True,
    )

    def __str__(self):
        return self.size

    def save(self, *args, **kwargs):
        if not self.size:
            self.size = "Skladem"
        super().save(*args, **kwargs)


# import PIL for image resizing


class Photo(models.Model):
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="photos"
    )
    photo = models.ImageField(upload_to="catalog/%Y/%m/%d")

    # resizing the image, you can change parameters like size and quality.
    def save(self, *args, **kwargs):
        super(Photo, self).save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 1125 or img.width > 1125:
            img.thumbnail((1125, 1125))
        # Force the image to be in an upright position (vertical)
        img = ImageOps.exif_transpose(img)
        img = img.rotate(0, expand=True)

        img.save(self.photo.path, quality=70, optimize=True)


# https://mailtrap.io/blog/django-contact-form/
class ContactForm(models.Model):
    name = models.CharField(max_length=50, verbose_name="Jméno")
    email = models.CharField(
        max_length=50, validators=[EmailValidator()], verbose_name="Email"
    )
    message = models.TextField(blank=True, verbose_name="Zpráva")

    def __str__(self):
        return self.message


class ProductSet(models.Model):
    # Common and specific fields for ProductSet
    product = models.ForeignKey(
        "catalog.Product",
        related_name="product_set",
        on_delete=models.CASCADE,
    )  # one to one relationship, each product has one inventory record
    kalhotky = models.ManyToManyField("Product", related_name="kalhotky", blank=True)
    podprsenky = models.ManyToManyField(
        "Product", related_name="podprsenky", blank=True
    )
    podvazkove_pasy = models.ManyToManyField(
        "Product", related_name="podvazkove_pasy", blank=True
    )

    class Meta:
        verbose_name = "Product Set"
        verbose_name_plural = "Product Sets"

    def get_kalhotky_sizes(self):
        kalhotky_sizes = self.kalhotky.values_list(
            "inventory__size", flat=True
        ).distinct()
        return list(kalhotky_sizes)

    def get_podprsenky_sizes(self):
        podprsenky_sizes = self.podprsenky.values_list(
            "inventory__size", flat=True
        ).distinct()
        return list(podprsenky_sizes)

    def get_pas_sizes(self):
        pas_sizes = self.podvazkove_pasy.values_list(
            "inventory__size", flat=True
        ).distinct()
        return list(pas_sizes)

    def __str__(self):
        return f"{self.product.name}"


class Certificate(models.Model):
    product = models.ForeignKey(
        "catalog.Product",
        related_name="certificate",
        on_delete=models.CASCADE,
    )  # one

    DISCOUNT_TYPES = [
        ("Procento", "Procento"),
        ("Částka", "Částka"),
    ]
    discount_type = models.CharField(
        max_length=255,
        choices=DISCOUNT_TYPES,
        verbose_name="Typ slevy",
        blank=True,
    )
    discount_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Zadejte hodnotu 0. anebo absolutní hodnotu částky",
        blank=True,
        default=0,
    )
    discount_threshold = models.DecimalField(
        verbose_name="Minimální částka pro uplatnění slevy",
        max_digits=10,
        decimal_places=0,
        blank=True,
        default=0,
        null=True,
    )
