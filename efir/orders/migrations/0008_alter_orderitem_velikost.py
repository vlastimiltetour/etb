# Generated by Django 4.2.3 on 2023-11-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0007_orderitem_kalhotky_velikost_set_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="velikost",
            field=models.CharField(
                blank=True,
                max_length=50,
                null=True,
                verbose_name="Individuální velikost",
            ),
        ),
    ]
