from django.urls import path

from . import views

app = "stripepayment"

urlpatterns = [
    path("process/", views.payment_process, name="process"),
    path("completed/", views.payment_completed, name="completed"),
    path("canceled/", views.payment_canceled, name="canceled"),
    path("notify/", views.payment_notification, name="payment_notification"),
]
