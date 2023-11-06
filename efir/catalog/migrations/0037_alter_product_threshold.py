# Generated by Django 4.2.3 on 2023-11-06 21:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0036_alter_product_threshold_alter_product_value"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="threshold",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                default=0,
                max_digits=10,
                null=True,
                verbose_name="Minimální částka pro uplatnění slevy",
            ),
        ),
    ]