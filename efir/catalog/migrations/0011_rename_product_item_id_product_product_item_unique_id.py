# Generated by Django 4.2.3 on 2023-08-27 09:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0010_product_product_item_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="product_item_id",
            new_name="product_item_unique_id",
        ),
    ]