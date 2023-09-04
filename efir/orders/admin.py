from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = (
        "order",
        "product",
        "price",
        "quantity",
        "obvod_hrudnik",
        "obvod_prsa",
        "obvod_boky",
    )
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "product_name",
        "etb_id",
        "velikosti",
        "total_cost",
        "discount",
        "quantity",
        "first_name",
        "last_name",
        "email",
        "number",
        "comments",
        "shipping",
        "address",
    ]
    inlines = [OrderItemInline]

    def get_total_cost(self, obj):
        return obj.get_total_cost()  # Call the Order's get_total_cost() method

    get_total_cost.short_description = (
        "Total Cost"  # Set the column header in the admin site
    )

    def product_name(self, obj):
        product_name = obj.items.first().product.name
        return product_name

    def price(self, obj):
        price_value = obj.items.values_list("price").first()
        return str(price_value[0])

    def quantity(self, obj):
        quantity_value = obj.items.values_list("quantity").first()
        return str(quantity_value[0])

    def velikosti(self, obj):
        items = obj.items.all()
        item_details = []
        for item in items:
            item_details.append(
                f"Pas: {item.obvod_hrudnik}, Podprsenka: {item.obvod_prsa}, Kalhotky: {item.obvod_boky}, Body: {item.obvod_body}"
            )
        print(item_details)
        return ", ".join(item_details)

    def druh_kolekce(self, obj):
        value = 0
        return str(value)

    velikosti.short_description = "Order Items"

    # Override the has_add_permission method to deny adding new records
    def has_add_permission(self, request):
        return False

    # Override the has_change_permission method to deny editing records
    def has_change_permission(self, request, obj=None):
        return False

    # Override the has_delete_permission method to deny deleting records
    def has_delete_permission(self, request, obj=None):
        return False
