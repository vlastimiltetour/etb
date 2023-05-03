from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("katalog", views.catalog_product_list, name="katalog"),
    path("kontakty", views.kontakty, name="kontakty"),
]
