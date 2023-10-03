from django.contrib import admin

from inventory.models import Inventory

from .models import Category, Photo, Product, ZpusobVyroby


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
        "limited",
        "get_available_sizes_display"
        # "display_velikost_produktu",
    ]
    exclude = ("poznamka",)  # Add this line to exclude the 'velikost' field

    actions = ["delete_selected", "custom_edit_action"]

    prepopulated_fields = {"slug": ("name",)}
    list_filter = ["bestseller"]

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

    class Meta:
        model = Product

    """ def display_velikost_produktu(self, obj):
        return ", ".join(str(obvod) for obvod in obj.velikost.all())

    display_velikost_produktu.short_description = "Velikost Produktu"
    """


@admin.register(ZpusobVyroby)
class ZpusobVyrobyAdmin(admin.ModelAdmin):
    list_display = ["size"]
    ordering = ["size"]
    actions = ["delete_selected"]

    def delete_selected(self, request, queryset):
        # Perform the delete operation on the selected queryset
        queryset.delete()

    delete_selected.short_description = "Delete selected ZpusobVyroby"
