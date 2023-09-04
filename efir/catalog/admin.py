from django.contrib import admin

from .models import (Body, Category, ObvodBoky, ObvodHrudnik, ObvodPrsa, Photo,
                     Product, ProductSize, ZpusobVyroby)


# Register your models here.
class PhotoAdmin(admin.StackedInline):
    model = Photo


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
        "limited",
        "display_obvod_hrudnik",
        "display_obvod_prsa",
        "display_obvod_boky",
    ]

    actions = ["delete_selected", "custom_edit_action"]

    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["bestseller"]

    def display_obvod_hrudnik(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_hrudnik.all())

    def display_obvod_prsa(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_prsa.all())

    def display_obvod_boky(self, obj):
        return ", ".join(str(obvod) for obvod in obj.obvod_boky.all())

    display_obvod_hrudnik.short_description = "Obvod Hrudnik"
    display_obvod_prsa.short_description = "Obvod Prsa"
    display_obvod_boky.short_description = "Obvod Boky"

    inlines = [PhotoAdmin]  # this is creating inline to show photos

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        size_types = ["obvod_prsa", "obvod_hrudnik", "obvod_boky"]

        if db_field.name in size_types:
            existing_choices = db_field.get_choices(include_blank=False)
            unique_choices_dict = {value: label for value, label in existing_choices}
            unique_choices = [
                (value, label) for value, label in unique_choices_dict.items()
            ]

            kwargs["choices"] = unique_choices

        return super().formfield_for_choice_field(db_field, request, **kwargs)

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


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ["product"]
