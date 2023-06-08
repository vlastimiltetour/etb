# Generated by Django 4.2 on 2023-06-05 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("email", models.CharField(max_length=50)),
                ("number", models.CharField(max_length=20)),
                ("comments", models.TextField(blank=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "shipping",
                    models.CharField(
                        choices=[("Z", "Zásilkovna"), ("O", "Osobní odběr")],
                        max_length=100,
                    ),
                ),
                ("address", models.CharField(max_length=250)),
            ],
            options={
                "ordering": ["-created"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="catalog.product",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="order",
            index=models.Index(
                fields=["-created"], name="orders_orde_created_743fca_idx"
            ),
        ),
    ]
