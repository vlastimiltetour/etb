# Generated by Django 4.2.3 on 2024-06-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0015_alter_order_shipping"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="certificate_from",
            field=models.CharField(default="-", max_length=100, verbose_name="Od koho"),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="certificate_to",
            field=models.CharField(default="-", max_length=100, verbose_name="Komu"),
        ),
    ]