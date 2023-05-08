from django.contrib import admin

from .models import Category, Product, ProductSize


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


admin.site.register(ProductSize)


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]
    list_editable = [
        "name",
    ]
    ordering = [
        "name",
    ]
