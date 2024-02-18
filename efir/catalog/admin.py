from django.contrib import admin

from inventory.models import Inventory

from .models import (BackgroundPhoto, Category, Certificate, LeftPhoto, Photo,
                     Product, ProductSet, RightdPhoto, UniqueSetCreation,
                     ZpusobVyroby)


# Register your models here.
class PhotoAdmin(admin.StackedInline):
    model = Photo


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 0


class InventoryInline(admin.TabularInline):
    model = Inventory
    extra = 1


@admin.register(BackgroundPhoto)
class BackgroundPhotoAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(LeftPhoto)
class LeftPhotoAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(RightdPhoto)
class RightPhotoAdmin(admin.ModelAdmin):
    list_display = ["name"]


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
        "active",
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

    inlines = [
        PhotoAdmin,
        InventoryInline,
        CertificateInline,
    ]  # this is creating inline to show photos

    def get_inline_instances(self, request, obj=None):
        # Only show CertificateInline if the product's category is "darkove certifikaty"

        if obj and obj.category and obj.category.name == "Dárkové certifikáty":
            return [CertificateInline(self.model, self.admin_site)]
        elif obj and obj.category and obj.category.name != "Dárkové certifikáty":
            return PhotoAdmin(self.model, self.admin_site), InventoryInline(
                self.model, self.admin_site
            )

        return (
            CertificateInline(self.model, self.admin_site),
            PhotoAdmin(self.model, self.admin_site),
            InventoryInline(self.model, self.admin_site),
        )

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


class UniqueSetCreationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "surname",
        "birthday",
        "hair_color",
        "skin_color",
        "color_tone",
        "colors_to_avoid",
        "design_preferences",
        "individual_cut",
        "knickers_cut",
        "bra_cut",
        "activities",
        "preferred_details",
        "gdpr_consent",
        #"newsletter_consent",
    )


admin.site.register(UniqueSetCreation, UniqueSetCreationAdmin)
