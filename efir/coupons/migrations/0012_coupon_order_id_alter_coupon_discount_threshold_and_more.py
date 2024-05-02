# Generated by Django 4.2.3 on 2024-05-01 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("coupons", "0011_alter_coupon_capacity"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="order_id",
            field=models.CharField(
                default="N/A", max_length=10, verbose_name="Nakoupeno v objednavce ID"
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="discount_threshold",
            field=models.DecimalField(
                decimal_places=0,
                default=0,
                max_digits=10,
                null=True,
                verbose_name="Minimální částka pro uplatnění slevy",
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="discount_value",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                max_digits=10,
                verbose_name="Zadejte hodnotu 0. anebo absolutní hodnotu částky",
            ),
        ),
    ]
