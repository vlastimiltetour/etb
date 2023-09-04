"""
from .models import Stock

# Register your models here.


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("product", "current_quantity", "last_updated")
"""
