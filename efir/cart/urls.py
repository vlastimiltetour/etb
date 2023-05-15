from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("pridat/<int:product_id>", views.cart_add, name="cart_add"),
    path("odebrat/<int:product_id>", views.cart_remove, name="cart_remove"),
    path("detail", views.cart_detail, name="cart_detail"),
]
