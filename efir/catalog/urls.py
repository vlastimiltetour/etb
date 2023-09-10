from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.home, name="home"),
    path("kontakty", views.kontakty, name="kontakty"),
    path("doprava", views.doprava, name="doprava"),
    path("reklamace", views.reklamace, name="reklamace"),
    path("rozmery", views.rozmery, name="rozmery"),
    path("ochrana-osobnich-udaju", views.ochrana, name="ochrana"),
    path("obchodni-podminky", views.obchodni_podminky, name="obchodni_podminky"),
    path("o-nas", views.about, name="about"),
    path("katalog", views.catalog_product_list, name="katalog_vse"),
    path(
        "<slug:category_slug>",
        views.catalog_product_list,
        name="product_list_by_category",
    ),
    path("<int:id>/<slug:slug>", views.product_detail, name="product_detail"),
]
