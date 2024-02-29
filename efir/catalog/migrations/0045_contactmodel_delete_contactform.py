# Generated by Django 4.2.3 on 2024-02-26 14:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0044_uniquesetcreation_newsletter_consent"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50, verbose_name="Jméno")),
                (
                    "email",
                    models.CharField(
                        max_length=50,
                        validators=[django.core.validators.EmailValidator()],
                        verbose_name="Email",
                    ),
                ),
                ("message", models.TextField(blank=True, verbose_name="Zpráva")),
            ],
        ),
        migrations.DeleteModel(
            name="ContactForm",
        ),
    ]