# Generated by Django 4.2.3 on 2023-08-15 06:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0003_remove_product_stock_quantity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="name",
            field=models.CharField(default="Celé sety", max_length=255),
        ),
    ]