# Generated by Django 4.2.3 on 2023-11-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupons", "0009_coupon_capacity"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="capacity",
            field=models.IntegerField(default=1),
        ),
    ]
