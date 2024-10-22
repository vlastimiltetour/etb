from django.contrib import admin
from stock.models import Stock

from .models import (Body, Category, ObvodBoky, ObvodHrudnik, ObvodPrsa, Photo,
                     Product, ZpusobVyroby)


# Register your models here.
class PhotoAdmin(admin.StackedInline):
    model = Photo


class StockInline(admin.TabularInline):
    model = Stock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "category",
        "price",
        "available",
        "display_stock_quantity",
        "display_obvod_hrudnik",
        "display_obvod_prsa",
        "display_obvod_boky",
    ]
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["bestseller"]

    def display_obvod_hrudnik(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_hrudnik.all())

    def display_obvod_prsa(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_prsa.all())

    def display_obvod_boky(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_boky.all())

    def display_stock_quantity(self, obj):
        stock_entries = Stock.objects.filter(product=obj)
        total_quantity = sum(entry.current_quantity for entry in stock_entries)
        return total_quantity

    display_obvod_hrudnik.short_description = "Obvod Hrudnik"
    display_obvod_prsa.short_description = "Obvod Prsa"
    display_obvod_boky.short_description = "Obvod Boky"

    inlines = [PhotoAdmin, StockInline]  # this is creating inline to show photos

    class Meta:
        model = Product


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


@admin.register(ObvodBoky)
class ObvodBokyAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = [
        "size",
    ]


@admin.register(Body)
class BodyAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = [
        "size",
    ]


@admin.register(ZpusobVyroby)
class ZpusobVyrobyAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = ["size"]
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        # Perform the delete operation on the selected queryset
        queryset.delete()

    delete_selected.short_description = "Delete selected ZpusobVyroby"
