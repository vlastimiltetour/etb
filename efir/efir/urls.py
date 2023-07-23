"""efir URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin", admin.site.urls),
    path("", include("catalog.urls")),
    path(
        "payments/", include(("payments.urls", "payments"), namespace="payments")
    ),  # this is very important, because the data structure is This code uses a 2-tuple with the URL patterns and app_name to include the 'payments' URLs.
    path("stripepayment/", include(("stripepayment.urls", "stripepayment"), namespace="stripepayment")),
    path("cart/", include("cart.urls")),
    path("orders/", include("orders.urls")),
    path("coupons/", include("coupons.urls")),
]

# and is used to serve static files (such as images, CSS files, and JavaScript files) during development.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
