from django.urls import path

from . import views

app_name = "newsletter"

urlpatterns = [
    path("subscribe", views.subscribe, name="subscribe"),
    path("unsubscribe", views.unsubscribe, name="unsubscribe"),
    path("subscribe_test", views.subscribe_test, name="subscribe_test"),
]
