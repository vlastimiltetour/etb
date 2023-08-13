from django.shortcuts import get_object_or_404, render

from cart.forms import CartAddProductForm
from orders.mail_confirmation import *

from .models import Category, Product


# returns home landing page
def home(request, category_slug=None):
    # zasilkovna_create_package()
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    best_sellers = Product.objects.filter(bestseller=True)

    # print(packetLabelPdf(4382587054, format="A7 on A4", offset=0))

    return render(
        request,
        "catalog/home.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "best_sellers": best_sellers,
        },
    )


# returns product list
def catalog_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)  # filtering available products

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    else:
        pass
    return render(
        request,
        "catalog/catalog.html",
        {"category": category, "categories": categories, "products": products},
    )


def product_detail(
    request,
    id,
    slug,
):
    categories = (
        Category.objects.all()
    )  # this is only for the purpose of showing the variable in the menu and footer
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    form = CartAddProductForm(id_from_product=id)

    return render(
        request,
        "catalog/product_detail.html",
        {
            "categories": categories,
            "product": product,
            "form": form,
        },
    )


def kontakty(request):
    categories = Category.objects.all()
    return render(request, "catalog/kontakty.html", {"categories": categories})


def about(request):
    categories = Category.objects.all()
    return render(request, "catalog/about.html", {"categories": categories})


def ochrana(request):
    categories = Category.objects.all()
    return render(request, "catalog/ochrana.html", {"categories": categories})
