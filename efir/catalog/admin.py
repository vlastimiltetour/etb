from django.contrib import admin

from inventory.models import Inventory

from .models import (Category, Certificate, Photo, Product, ProductSet,
                     ZpusobVyroby)


# Register your models here.
class PhotoAdmin(admin.StackedInline):
    model = Photo


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1


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
        "get_available_sizes_display",
        "new",
        "bestseller",
        "headliner",
        "limited",
        # "display_velikost_produktu",
    ]
    exclude = ("poznamka",)  # Add this line to exclude the 'velikost' field

    actions = ["delete_selected", "custom_edit_action"]

    prepopulated_fields = {"slug": ("name",)}
    list_filter = [
        "name",
        "category",
        "price",
        "new",
        "bestseller",
        "headliner",
        "limited",
        # "display_velikost_produktu",
    ]

    inlines = [PhotoAdmin, InventoryInline]  # this is creating inline to show photos

    def get_available_sizes_display(self, obj):
        # Display a comma-separated string of available sizes for each product
        sizes = obj.get_available_sizes()
        return ", ".join(sizes)

    get_available_sizes_display.short_description = "Available Sizes"

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        size_types = ["velikost"]

        if db_field.name in size_types:
            existing_choices = db_field.get_choices(include_blank=False)
            unique_choices_dict = {value: label for value, label in existing_choices}
            unique_choices = [
                (value, label) for value, label in unique_choices_dict.items()
            ]

            kwargs["choices"] = unique_choices

        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        # Customize saving behavior based on the selected category

        if obj.category and obj.category.name == "Dárkové certifikáty":
            # If the category is "Dárkové certifikáty", create the product first
            super().save_model(request, obj, form, change)

            # Then, create or update the Inventory with size "-"
            inventory, created = Inventory.objects.get_or_create(
                product=obj, size="-", defaults={"quantity": 1}
            )

            if not created:
                # If the inventory entry already exists, update the quantity
                # Manually set ZpusobVyroby to "-"

                inventory.quantity = 1
                inventory.save()
            else:
                # For other categories, proceed with the default saving behavior
                super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)

    class Meta:
        model = Product


@admin.register(ZpusobVyroby)
class ZpusobVyrobyAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = ["size"]
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        # Perform the delete operation on the selected queryset
        queryset.delete()

    delete_selected.short_description = "Delete selected ZpusobVyroby"


@admin.register(ProductSet)
class ProductSetAdmin(admin.ModelAdmin):
    list_display = ["product"]


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ["product"]
