# Generated by Django 4.2.3 on 2023-11-04 14:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupons", "0005_alter_coupon_discount"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="percentage_discount",
            field=models.IntegerField(
                blank=True,
                default=0,
                help_text="Sleva v procentech 0 az 100",
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ],
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="coupon",
            name="discount",
            field=models.DecimalField(
                blank=True,
                decimal_places=0,
                max_digits=10,
                verbose_name="Hodnota slevy",
            ),
        ),
    ]