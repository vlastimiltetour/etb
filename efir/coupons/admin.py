from django.contrib import admin

from .models import Coupon


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "order_id",
        "valid_from",
        "valid_to",
        "discount_type",
        "active",
        "redeemed",
        "discount_threshold",
        "capacity",
        "discount_value",
        "certificate_from",
        "certificate_to",
    ]
    list_filter = ["active", "valid_from", "valid_to"]
    search_fields = ["code"]
