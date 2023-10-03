# Register your models here.
# Register your models here.
from django.contrib import admin
from django.db.models import Sum

from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ["product", "size", "quantity"]

    list_editable = ["quantity"]


