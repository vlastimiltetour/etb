# Generated by Django 4.2.3 on 2024-05-11 22:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0009_orderitem_certificate_from_orderitem_certificate_to_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="shipping",
            field=models.CharField(
                choices=[("Z", "Zásilkovna"), ("O", "Online")],
                default="Zásilkovna",
                max_length=100,
                verbose_name="Doprava",
            ),
        ),
    ]
