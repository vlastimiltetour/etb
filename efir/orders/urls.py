from django.urls import path

from . import views
from .views import *

app_name = "orders"


urlpatterns = [
    path(
        "objednavka_vytvorena", views.objednavka_vytvorena, name="objednavka_vytvorena"
    ),
    path(
        "media/assets/<str:file_name>",
        views.download_ppl_label,
        name="download_ppl_label",
    ),
    path("new", views.new_order, name="new_order"),
]
