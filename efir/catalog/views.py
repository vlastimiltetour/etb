from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, "catalog/home.html")


def catalog_product_list(request, category_slug=None):
    
    return render(request, "catalog/catalog.html")


def product_detail(request, id, slug):
    return render(request, "catalog/product_detail.html")


def kontakty(request):
    return render(request, "catalog/kontakty.html")
