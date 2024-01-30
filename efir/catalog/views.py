import logging
import ssl

from django.shortcuts import get_object_or_404, render

logging.basicConfig(level=logging.DEBUG)

from django.db.models import Q

from cart.forms import CartAddProductForm
from catalog.forms import ContactForm
from inventory.models import Inventory
from orders.mail_confirmation import *
from stripepayment.views import *

from .models import (BackgroundPhoto, Category, LeftPhoto, Product, ProductSet,
                     RightdPhoto)


# returns home landing page
def home(request, category_slug=None):
    # zasilkovna_create_package(order_id=1)
    # customer_order_email_confirmation(order_id=143)
    # packetLabelPdf(2336806921, format="A7 on A4", offset=0)
    # order = Order.objects.get(id=1)
    # print(order.total_cost)
    # print(coupon_create(request.GET, 500.00))
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(active=True)[:9]
    best_sellers = Product.objects.filter(bestseller=True, active=True)
    novinky = Product.objects.filter(new=True, active=True)
    productsets = ProductSet.objects.all()
    backgroundphoto = BackgroundPhoto.objects.all()
    leftphoto = LeftPhoto.objects.all()
    rightphoto = RightdPhoto.objects.all()

    # print(packetLabelPdf(4382587054, format="A7 on A4", offset=0))

    return render(
        request,
        "catalog/home.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "best_sellers": best_sellers,
            "productsets": productsets,
            "backgroundphoto": backgroundphoto,
            "leftphoto": leftphoto,
            "rightphoto": rightphoto,
            "novinky": novinky,
        },
    )


def catalog_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(active=True)  # filtering available products
    inventory = Inventory.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category, active=True)


    return render(
        request,
        "catalog/catalog.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "inventory": inventory,
        },
    )


def product_detail(
    request,
    id,
    slug,
):
    categories = (
        Category.objects.all()
    )  # this is only for the purpose of showing the variable in the menu and footer
    product = get_object_or_404(Product, id=id, slug=slug)
    form = CartAddProductForm(id_from_product=id)

    recommended = recommended_products(product_id=id)
    print(
        f"this is the product id of the product {product.name}, {id} and recommended products  {recommended}"
    )

    if str(product.category) == "Dárkové certifikáty":
        pass

    try:
        productset = ProductSet.objects.get(product=product)
    except ProductSet.DoesNotExist:
        productset = None

    return render(
        request,
        "catalog/product_detail.html",
        {
            "categories": categories,
            "product": product,
            "form": form,
            "productset": productset,
            "recommended": recommended,
        },
    )


def doprava(request):
    categories = Category.objects.all()
    return render(request, "catalog/doprava.html", {"categories": categories})


def rozmery(request):
    categories = Category.objects.all()
    return render(request, "catalog/rozmery.html", {"categories": categories})


def reklamace(request):
    categories = Category.objects.all()
    return render(request, "catalog/reklamace.html", {"categories": categories})


def about(request):
    categories = Category.objects.all()
    return render(request, "catalog/about.html", {"categories": categories})


def ochrana(request):
    categories = Category.objects.all()
    return render(request, "catalog/ochrana.html", {"categories": categories})


def obchodni_podminky(request):
    categories = Category.objects.all()
    return render(request, "catalog/obchodni_podminky.html", {"categories": categories})


from django.template.loader import render_to_string


# https://mailtrap.io/blog/django-contact-form/
def kontakty(request):
    categories = Category.objects.all()
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            success_message = "Your message has been successfully submitted."

            html_content = render_to_string("orders/contact_form.html")
            msg = EmailMultiAlternatives(
                subject=(f"Kontaktní formulář: dotaz od {name}"),
                from_email="objednavky@efirthebrand.cz",
                to=[email, "objednavky@efirthebrand.cz"],
            )
            msg.attach_alternative(html_content, "text/html")
            try:
                msg.send()

            except ssl.SSLCertVerificationError:
                logging.info(
                    f"Local environment has no email backend set up {name, email, message}. "
                )

            return render(
                request,
                "catalog/kontakty_success.html",
                {
                    "categories": categories,
                    "form": form,
                    "success_message": success_message,
                },
            )

    else:
        form = ContactForm()

    return render(
        request,
        "catalog/kontakty.html",
        {"categories": categories, "form": form},
    )


def recommended_products(product_id):
    product_id = product_id

    recommendations = Product.objects.filter(Q(bestseller=True))
    print(f"These are the recommended products: {recommendations}")
    # recommendations = best_sellers[:5]

    return recommendations[:5]
