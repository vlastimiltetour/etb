from django.urls import path

from . import views

urlpatterns = [
    path("kosik", views.kosik, name="kosik"),
]
