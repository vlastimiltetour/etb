from django.urls import path

from . import views

app_name = "cart"

urlpatterns = [
    path("pridat/<int:product_id>", views.cart_add, name="cart_add"),
    path("odebrat/<int:product_id>", views.cart_remove, name="cart_remove"),
    path("clean_cart_session", views.clean_cart_session, name="clean_cart_session"),
    path(
        "update_cart_quantity/<str:item_id>",
        views.update_cart_quantity,
        name="update_cart_quantity",
    ),
    path("detail", views.cart_detail, name="cart_detail"),
    path("update_cart_country/", views.update_cart_country, name="update_cart_country"),
]
