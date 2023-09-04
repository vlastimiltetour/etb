# Generated by Django 4.2.3 on 2023-08-16 18:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0006_orderitem_obvod_body_alter_order_vendor_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="country",
            field=models.CharField(
                choices=[("CZ", "Česko"), ("SK", "Slovensko")],
                max_length=20,
                verbose_name="Země",
            ),
        ),
    ]
