from django.urls import path

from . import views

app_name = "coupons"

urlpatterns = [
    path("apply", views.coupon_apply, name="apply"),
    path("delete", views.coupon_delete, name="delete"),
    path("create_coupon/", views.coupon_create, name="create_coupon"),
    # Add other URL patterns as needed
]
