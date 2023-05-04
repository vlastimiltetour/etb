from django.http import HttpResponse
from django.shortcuts import render

from .models import Category, Product

# Create your views here.


# returns home landing page
def home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(
        request,
        "catalog/home.html",
        {"category": category, "categories": categories, "products": products},
    )


# returns product list
def catalog_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(
        request,
        "catalog/catalog.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(request, id, slug):
    return render(request, "catalog/product_detail.html")


def kontakty(request):
    return render(request, "catalog/kontakty.html")
