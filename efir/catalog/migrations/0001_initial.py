# Generated by Django 4.2 on 2023-07-05 06:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255, unique=True)),
            ],
            options={
                "verbose_name": "category",
                "verbose_name_plural": "categories",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="ObvodBoky",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        default=0,
                        help_text="Dostupné konfekční velikosti",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ObvodHrudnik",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        default=0,
                        help_text="Dostupné konfekční velikosti",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ObvodPrsa",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(
                        default=0,
                        help_text="Dostupné konfekční velikosti",
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(max_length=255)),
                (
                    "image1",
                    models.ImageField(
                        default="/static/assets/img/dummyimage.jpeg",
                        upload_to="catalog/%Y/%m/%d",
                    ),
                ),
                (
                    "image2",
                    models.ImageField(
                        default="/static/assets/img/dummyimage.jpeg",
                        upload_to="catalog/%Y/%m/%d",
                    ),
                ),
                (
                    "image3",
                    models.ImageField(
                        default="/static/assets/img/dummyimage.jpeg",
                        upload_to="catalog/%Y/%m/%d",
                    ),
                ),
                (
                    "image4",
                    models.ImageField(
                        default="/static/assets/img/dummyimage.jpeg",
                        upload_to="catalog/%Y/%m/%d",
                    ),
                ),
                ("price", models.DecimalField(decimal_places=0, max_digits=10)),
                ("short_description", models.TextField(blank=True, max_length=50)),
                ("long_description", models.TextField(blank=True)),
                (
                    "zpusob_vyroby",
                    models.CharField(
                        choices=[("K", "Konfekční velikost"), ("N", "Na míru")],
                        max_length=100,
                        null=True,
                    ),
                ),
                ("new", models.BooleanField(default=False)),
                ("available", models.BooleanField(default=False)),
                ("discount", models.BooleanField(default=False)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("bestseller", models.BooleanField(default=False)),
                ("headliner", models.BooleanField(default=False)),
                ("product_return", models.BooleanField(default=False)),
                ("poznamka", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.category",
                    ),
                ),
                ("obvod_boky", models.ManyToManyField(to="catalog.obvodboky")),
                ("obvod_hrudnik", models.ManyToManyField(to="catalog.obvodhrudnik")),
                ("obvod_prsa", models.ManyToManyField(to="catalog.obvodprsa")),
            ],
            options={
                "ordering": ["name"],
            },
        ),
        migrations.AddIndex(
            model_name="category",
            index=models.Index(fields=["name"], name="catalog_cat_name_39f70b_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["id", "slug"], name="catalog_pro_id_a44864_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["name"], name="catalog_pro_name_f603c0_idx"),
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(
                fields=["-created"], name="catalog_pro_created_b92f5e_idx"
            ),
        ),
    ]
