from django.urls import path

from . import views

app_name = "coupons"

urlpatterns = [
    path("apply", views.coupon_apply, name="apply"),
    path("deactivate", views.coupon_deactivate, name="coupon_deactivate"),
    path("delete", views.coupon_delete, name="delete"),
    path("create_coupon/", views.coupon_create, name="create_coupon"),
    path("generate_vouchers", views.generate_vouchers, name="generate_vouchers"),
    path("repair_vouchers", views.repair_vouchers, name="repair_vouchers"),

    # Add other URL patterns as needed
]
