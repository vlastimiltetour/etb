from django.urls import path

from . import views, webhooks

app = "stripepayment"

urlpatterns = [
    path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("notify/", views.payment_notification, name="payment_notification"),
    path("packetapdf/", views.packetLabelPdf, name="packetLabelPdf"),
    path("webhook/", webhooks.stripe_webhook, name="stripe_webhook"),
    path(
        "zasilkovna-create-package/",
        views.zasilkovna_create_package,
        name="zasilkovna_create_package",
    ),
]
