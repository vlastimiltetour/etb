from django.urls import path

from . import views
from .views import *

app_name = "orders"


urlpatterns = [
    path(
        "objednavka_vytvorena", views.objednavka_vytvorena, name="objednavka_vytvorena"
    ),
    path("invoice", views.invoice, name="invoice"),
    path("contact_form", views.contact_form, name="contact_form"),
    path(
        "media/assets/<str:file_name>",
        views.download_ppl_label,
        name="download_ppl_label",
    ),
    path("new", views.new_order, name="new_order"),
    path("send_offer_confirmation/<int:order_id>/", views.send_offer_confirmation, name="send_offer_confirmation"),

]
