from django.db import models
from django.urls import reverse  # this is when calling an address by name


# Create your models here.
class Product(models.Model):
    # Product specifics
    category = models.ForeignKey(
        "Category",
        related_name="products",
        on_delete=models.CASCADE,
    )  # one to many relationship, a product belongs to one category and a category contains multiple products
    # So if you have a Category instance cat, you can access all the related Product instances by calling
    # cat.products.all()
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=False)
    image = models.ImageField(
        upload_to="catalog/%Y/%m/%d", default="/static/assets/img/dummyimage.jpeg"
    )
    price = models.DecimalField(max_digits=10, decimal_places=0)
    description = models.TextField(blank=True)

    # Time Specifics
    new = models.BooleanField(default=False)
    available = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    bestseller = models.BooleanField(default=False)
    headliner = models.BooleanField(default=False)
    product_return = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["id", "slug"]),
            models.Index(fields=["name"]),
            models.Index(fields=["-created"]),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product_detail", args=[self.id, self.slug])


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, null=False, unique=True
    )  # unique creates an index

    # additional information about Category model
    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(
                fields=["name"]
            ),  # this piece of code improves query performance
        ]
        verbose_name = "category"  # provides human readable names
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(
        self,
    ):
        return reverse("product_list_by_category", args=[self.slug])
