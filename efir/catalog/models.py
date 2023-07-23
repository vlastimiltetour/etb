from django.db import models
from django.urls import reverse  # this is when calling an address by name


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
    available = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    bestseller = models.BooleanField(default=False)
    headliner = models.BooleanField(default=False)

    obvod_hrudnik = models.ManyToManyField(
        "ObvodHrudnik", blank=True, verbose_name="velikost pasu", default="-"
    )
    obvod_prsa = models.ManyToManyField(
        "ObvodPrsa", blank=True, verbose_name="velikost podprsenky", default="-"
    )
    obvod_boky = models.ManyToManyField(
        "ObvodBoky", blank=True, verbose_name="velikost kalhotek", default="-"
    )
    obvod_body = models.ManyToManyField(
        "Body", blank=True, verbose_name="velikost body", default="-"
    )

    zpusob_vyroby = models.ManyToManyField(
        "ZpusobVyroby", blank=True, verbose_name="Druh kolekce"
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.id, self.slug])


class Category(models.Model):
    CATEGORY_CHOICES = [
        ("Celé sety", "Celé sety"),
        ("Podprsenky", "Podprsenky"),
        ("Kalhotky", "Kalhotky"),
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
        return reverse("product_list_by_category", args=[self.slug])


class ObvodHrudnik(models.Model):
    OBVOD_HRUDNIK_CHOICES = [(str(i), str(i)) for i in ["XS", "S", "M", "L"]]

    size = models.CharField(
        max_length=20,
        help_text="Dostupné konfekční velikosti",
        blank=True,
        choices=OBVOD_HRUDNIK_CHOICES,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "velikost pasu"
        verbose_name_plural = "velikosti pasu"


class ObvodPrsa(models.Model):
    OBVOD_PRSA_CHOICES = [
        (str(i) + j, str(i) + j) for i in range(70, 110, 5) for j in ["A", "B", "C"]
    ]

    size = models.CharField(
        max_length=20,
        help_text="Dostupné konfekční velikosti",
        blank=True,
        choices=OBVOD_PRSA_CHOICES,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "velikost podprsenky"
        verbose_name_plural = "velikost podprsenky"


class ObvodBoky(models.Model):
    OBVOD_BOKY_CHOICES = [(str(i), str(i)) for i in ["XS", "S", "M", "L"]]
    size = models.CharField(
        max_length=20,
        help_text="Dostupné konfekční velikosti",
        blank=True,
        choices=OBVOD_BOKY_CHOICES,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "velikost kalhotek"
        verbose_name_plural = "velikosti kalhotek"


class Body(models.Model):
    size = models.CharField(
        max_length=20,
        help_text="Dostupné konfekční velikosti",
        blank=True,
    )

    def __str__(self):
        return self.size

    class Meta:
        verbose_name = "velikost body"
        verbose_name_plural = "velikosti body"


class ZpusobVyroby(models.Model):
    ZPUSOB_VYROBY_CHOICES = [
        ("Konfekce", "Konfekce"),
        ("Na Míru", "Na Míru"),
    ]

    size = models.CharField(
        max_length=20,
        choices=ZPUSOB_VYROBY_CHOICES,
        default="Konfekční velikost",
        blank=True,
    )

    def __str__(self):
        return self.size


# import PIL for image resizing
from PIL import Image


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
        img.save(self.photo.path, quality=70, optimize=True)
