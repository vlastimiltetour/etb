import logging
import ssl

from django.shortcuts import get_object_or_404, render

logging.basicConfig(level=logging.DEBUG)

from cart.forms import CartAddProductForm
from catalog.forms import ContactForm
from orders.mail_confirmation import *
from stripepayment.views import *

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
    products = Product.objects.all()  # filtering available products

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
    product = get_object_or_404(Product, id=id, slug=slug)

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

            html_content = render_to_string("orders/customer_email_confirmation.html")
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
