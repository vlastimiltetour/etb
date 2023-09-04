# Generated by Django 4.2.3 on 2023-08-17 17:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0006_alter_zpusobvyroby_size"),
        ("orders", "0009_alter_orderitem_obvod_body_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="obvod_body",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.body",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="obvod_boky",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.obvodboky",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="obvod_hrudnik",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.obvodhrudnik",
            ),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="obvod_prsa",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="catalog.obvodprsa",
            ),
        ),
    ]
