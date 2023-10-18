# Generated by Django 4.2.3 on 2023-10-01 19:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("catalog", "0019_alter_product_obvod_body_alter_product_obvod_boky_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Body",
            new_name="VelikostProduktu",
        ),
        migrations.AlterUniqueTogether(
            name="productsize",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="obvod_body",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="obvod_boky",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="obvod_hrudnik",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="obvod_prsa",
        ),
        migrations.RemoveField(
            model_name="productsize",
            name="product",
        ),
        migrations.AlterModelOptions(
            name="velikostproduktu",
            options={"verbose_name": "velikost"},
        ),
        migrations.RemoveField(
            model_name="product",
            name="obvod_body",
        ),
        migrations.RemoveField(
            model_name="product",
            name="obvod_boky",
        ),
        migrations.RemoveField(
            model_name="product",
            name="obvod_hrudnik",
        ),
        migrations.RemoveField(
            model_name="product",
            name="obvod_prsa",
        ),
        migrations.AddField(
            model_name="product",
            name="velikost",
            field=models.ManyToManyField(
                blank=True, to="catalog.velikostproduktu", verbose_name="velikost"
            ),
        ),
        migrations.DeleteModel(
            name="ObvodBoky",
        ),
        migrations.DeleteModel(
            name="ObvodHrudnik",
        ),
        migrations.DeleteModel(
            name="ObvodPrsa",
        ),
        migrations.DeleteModel(
            name="ProductSize",
        ),
    ]