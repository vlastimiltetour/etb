from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("kontakty", views.kontakty, name="kontakty"),
    path("o-nas", views.about, name="about"),
    path("katalog", views.catalog_product_list, name="katalog"),
    path(
        "<slug:category_slug>",
        views.catalog_product_list,
        name="product_list_by_category",
    ),
    path("<int:id>/<slug:slug>", views.product_detail, name="product_detail"),
]
