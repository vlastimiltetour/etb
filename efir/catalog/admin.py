from django.contrib import admin

from .models import Category, ObvodHrudnik, ObvodPrsa, Product

# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "slug",
        "price",
        "available",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["bestseller"]


@admin.register(ObvodHrudnik)
class ObvodHrudnikAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = [
        "size",
    ]


@admin.register(ObvodPrsa)
class ObvodPrsaAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = [
        "size",
    ]
