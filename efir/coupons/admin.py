from django.contrib import admin

from .models import Coupon
import xlwt

import csv
from datetime import datetime


from django.http import HttpResponse



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = [
        "code",
        "category",
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
    list_filter = ["active", "valid_from", "valid_to", "category"]
    search_fields = ["code"]


    @staticmethod
    def transfer_date(input_date):
        try:
            date = datetime.strptime(str(input_date), '%Y-%m-%d')
            transformed_date = date.strftime('%d.%m.%Y')  # Correct usage of strftime
            return transformed_date
        except ValueError:
            return "Invalid Format Date"

    def export_to_csv(self, request, queryset):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="coupons.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "code",
            "valid_to",  # Adjust header names as needed
        ])

        for obj in queryset:
            writer.writerow([
                obj.code,
                self.transfer_date(obj.valid_to),  # Call transfer_date method
            ])

        return response

    export_to_csv.short_description = "Exportovat kódy do Leadhub do CSV"

    actions = ["export_to_csv"]
