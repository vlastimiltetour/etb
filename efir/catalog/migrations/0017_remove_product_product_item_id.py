# Generated by Django 4.2.3 on 2023-09-10 13:29

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0016_alter_product_product_item_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="product_item_id",
        ),
    ]