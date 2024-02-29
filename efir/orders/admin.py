import xlwt
from django.contrib import admin
from django.http import HttpResponse

from .models import Order, OrderItem

from django.utils import timezone



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = (
        "order",
        "product",
        "velikost",
        "poznamka",
        "price",
        "quantity",
    )

    class Meta:
        ordering = ("product", "velikost", "price", "quantity", "order")

    def has_change_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "etb_id",
        "products",
        "total_cost",
        "paid",
        "shipped",
        # "discount",
        # "quantity",
        "first_name",
        "last_name",
        "email",
        # "birthday",
        "number",
        "newsletter_consent",
        "comments",
        "shipping",
        "address",
        "created",
    ]

    inlines = [OrderItemInline]

    # list_editable = ["shipped"]  # Add the "shipped" field to make it editable

    def get_total_cost(self, obj):
        return obj.get_total_cost()  # Call the Order's get_total_cost() method

    get_total_cost.short_description = (
        "Total Cost"  # Set the column header in the admin site
    )

    def products(self, obj):
        product_names = [item.product.name for item in obj.items.all()]
        return product_names

    def price(self, obj):
        price_value = obj.items.values_list("price").first()
        return str(price_value[0])

    def quantity(self, obj):
        quantity_value = obj.items.values_list("quantity").first()
        if (
            quantity_value is not None and quantity_value
        ):  # Check for both None and an empty list
            return str(quantity_value[0])
        else:
            return "N/A"  # or some default value

    def velikosti(self, obj):
        items = obj.items.all()
        item_details = []
        for item in items:
            item_details.append(f"{item.velikost}")
            item_details.append(f"kalhotky_velikost_set: {item.kalhotky_velikost_set}")
            item_details.append(
                f"podprsenka_velikost_set: {item.podprsenka_velikost_set}"
            )
            item_details.append(f"pas_velikost_set: {item.pas_velikost_set}")

        return ", ".join(item_details)

    def druh_kolekce(self, obj):
        value = 0
        return str(value)

    velikosti.short_description = "Položky v objednávce"

    def get_readonly_fields(self, request, obj=None):
        # Make all fields readonly except for "shipped"
        if obj:
            return [
                field.name
                for field in self.model._meta.fields
                if (field.name != "shipped" and field.name != "paid")
            ]
        else:
            return []

    def has_add_permission(self, request, obj=None):
        return False
        

    def export_to_excel(self, request, queryset):
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = 'attachment; filename="orders.xls"'

        wb = xlwt.Workbook(encoding="utf-8")
        ws = wb.add_sheet("Orders")

        row_num = 0

        columns = [
            "etb_id",
            "products",
            "total_cost",
            "paid",
            "shipped",
            "first_name",
            "last_name",
            "email",
            "number",
            "newsletter_consent",
            "comments",
            "shipping",
            "address",
        ]

        for col_num, column_title in enumerate(columns):
            ws.write(row_num, col_num, column_title)

        for obj in queryset:
            row_num += 1
            row = [
                obj.etb_id,
                ", ".join([item.product.name for item in obj.items.all()]),
                obj.get_total_cost(),
                obj.paid,
                obj.shipped,
                obj.first_name,
                obj.last_name,
                obj.email,
                obj.number,
                obj.newsletter_consent,
                obj.comments,
                obj.shipping,
                obj.address,
            ]
            for col_num, cell_value in enumerate(row):
                ws.write(row_num, col_num, cell_value)

        wb.save(response)
        return response

    export_to_excel.short_description = "Exportovat do Excelu"

    actions = ["export_to_excel"]
