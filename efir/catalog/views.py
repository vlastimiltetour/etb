import logging
import ssl

from django.shortcuts import get_object_or_404, redirect, render

logging.basicConfig(level=logging.DEBUG)

from django.db.models import Q

from cart.forms import CartAddProductForm
from catalog.forms import ContactForm, CreateSetForm, FilterForm
from inventory.models import Inventory
from orders.mail_confirmation import *
from stripepayment.views import *

from .models import (BackgroundPhoto, Category, ContactModel, LeftPhoto,
                     Product, ProductSet, RightdPhoto, UniqueSetCreation)


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
    products = Product.objects.filter(active=True, category__name="Celé sety")[:9]
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


def save_filters(request, category_slug=None):
    if request.method == "POST":
        filter_form = FilterForm(request.POST)
        # print(request.POST)  # Print the entire POST data for debugging

        if filter_form.is_valid():
            cd = filter_form.cleaned_data

            # these values are lists, wtf
            zpusob_vyroby = cd["zpusob_vyroby"]
            sort_by_price = cd["sort_by_price"]
            size_selection = cd["size_selection"]
            cut_selection = cd["cut_selection"]
            category_selection = cd["category_selection"]

            if category_selection != []:
                request.session["category_session"] = category_selection

            if zpusob_vyroby != []:
                request.session["zpusob_vyroby_session"] = zpusob_vyroby

            if sort_by_price != []:
                for value in sort_by_price:
                    request.session["sort_by_price_session"] = value

            if "size_selection_session" not in request.session:
                request.session["size_selection_session"] = []

            if size_selection:
                for val in size_selection:
                    if val not in request.session["size_selection_session"]:
                        request.session["size_selection_session"].append(val)
                        request.session.save()

            if "cut_selection_session" not in request.session:
                request.session["cut_selection_session"] = []

            # this is cut selection which allows more than 1
            # if cut_selection:
            #    for x in cut_selection:
            #        if x not in request.session["cut_selection_session"]:
            #            request.session["cut_selection_session"].append(x)
            #            request.session.save()

            # this is cut selection which allows only 1 value
            if cut_selection:
                for cut in cut_selection:
                    request.session["cut_selection_session"] = cut
                    request.session.save()

    return redirect("catalog:katalog_vse")


def show_session_contents(request):
    print("")
    print("Session Contents:")
    for key, value in request.session.items():
        print(f"{key}: {value}")

    print("")
    return "These were the session contents"


def catalog_product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    inventory = Inventory.objects.values("size").distinct().order_by("size")

    filter_form = FilterForm()

    zpusob_vyroby_session = request.session.get("zpusob_vyroby_session", "")
    size_selection_session = request.session.get("size_selection_session", [])
    sort_by_price_session = request.session.get("sort_by_price_session", "created")
    cut_selection_session = request.session.get("cut_selection_session", [])
    category_session = request.session.get("category_session", "")

    # these are session contents
    print(show_session_contents(request))

    query_filters = Q()

    if category_session:
        query_filters &= Q(category__name=category_session[0])

    if cut_selection_session:
        if type(cut_selection_session) == str:
            if cut_selection_session == "Brazilky":
                # Filter for products containing "Brazilky" but exclude those containing "Brazilky na gumičkách"
                query_filters &= Q(short_description__icontains="Brazilky")
                query_filters &= ~Q(short_description__icontains="Brazilky na gumičkách")
            elif cut_selection_session == "Podprsenka s kosticemi":
                # Filter for products containing "Brazilky" but exclude those containing "Brazilky na gumičkách"
                query_filters &= Q(short_description__icontains="Podprsenka s kosticemi")
                query_filters &= ~Q(short_description__icontains="Podprsenka s kosticemi a otevřeným košíčkem")

            else:
                query_filters &= Q(short_description__icontains=cut_selection_session)
        else:
            pass


        

    if zpusob_vyroby_session:
        query_filters &= Q(
            zpusob_vyroby__size=zpusob_vyroby_session[0]
        )  # Assuming zpusob_vyroby is a list

    if size_selection_session:
        query_filters &= Q(inventory__size__in=size_selection_session)

    if sort_by_price_session == ([] or None):
        sort_by_price_session = "created"
    elif type(sort_by_price_session) == str:
        sort_by_price_session = sort_by_price_session

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)

        products = (
            products.filter(category=category)
            .filter(query_filters)
            .order_by(sort_by_price_session)
        )

    else:
        products = Product.objects.filter(query_filters).order_by(sort_by_price_session).filter(active=True)

    sum_of = len(products)

    selected_sizes = clean_session_names(size_selection_session)
    selected_zpubob_vyroby = clean_session_names(zpusob_vyroby_session)
    selected_sorting = clean_session_names(sort_by_price_session)
    selected_cuts = clean_session_names(cut_selection_session)
    selected_category = clean_session_names(category_session)

    return render(
        request,
        "catalog/catalog.html",
        {
            "category": category,
            "categories": categories,
            "products": products,
            "inventory": inventory,
            "filter_form": filter_form,
            "selected_sizes": selected_sizes,
            "selected_zpubob_vyroby": selected_zpubob_vyroby,
            "selected_sorting": selected_sorting,
            "selected_cuts": selected_cuts,
            "selected_category": selected_category,
            "sum_of": sum_of,
        },
    )


def clean_session_names(session_values):
    clean_translation_dict = {
        "price": "Cena vzestupně",
        "-price": "Cena sestupně",
        "name": "Název A-Z",
        "-name": "Název Z-A",
        "created": "Nejnovější",
    }

    for key in clean_translation_dict:
        if key == session_values:
            session_values = clean_translation_dict[key]

    return (
        str(session_values)
        .replace("'", "")
        .replace("[", "")
        .replace("]", "")
        .replace("[", "")
        .replace("]", "")
    )


def delete_all_filters(request):
    if request.method == "POST":
        print("Before Deletion:", request.session.items())

        to_delete = [
            "zpusob_vyroby_session",
            "size_selection_session",
            "cut_selection_session",
            "category_session",
        ]
        for key in to_delete:
            if key in request.session:
                del request.session[key]

        if "sort_by_price_session" in request.session:
            request.session["sort_by_price_session"] = "created"

        print("After Deletion:", request.session.items())

    return redirect("catalog:katalog_vse")


def delete_selected_filter(request):
    if request.method == "POST":
        # print("Before Deletion:", request.session.items())

        sessions = [
            "zpusob_vyroby_session",
            "size_selection_session",
            "cut_selection_session",
            "category_session",
        ]

        clean_translation_dict = {
            "Cena vzestupně": "price",
            "Cena sestupně": "-price",
            "Název A-Z": "name",
            "Název Z-A": "-name",
        }

        selected_filter = request.POST.get("selected_filter")

        if selected_filter in clean_translation_dict:
            selected_filter = clean_translation_dict[selected_filter]
            if "sort_by_price_session" in request.session:
                request.session["sort_by_price_session"] = "created"

        for session_value in sessions:
            if session_value in request.session:
                keys = request.session[session_value]
                print("tady zaciname se session keys", keys)

                for key in keys:
                    try:
                        if key == selected_filter or key in selected_filter:
                            print("vytiskni mi u session value", session_value)
                            del request.session[session_value]
                    except KeyError:
                        print("hele tady je chyba KeyError", KeyError)

    return redirect("catalog:katalog_vse")


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
            print(form.errors)
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]
            success_message = "Your message has been successfully submitted."

            # Create a new instance of ContactModel and save it
            contact_model = ContactModel(name=name, email=email, message=message)
            contact_model.save()

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


def akce(request):
    products = Product.objects.all()
    discounted = Product.objects.exclude(discount__isnull=True)

    print("these are akce discounts:", discounted)

    return render(
        request, "catalog/akce.html", {"products": products, "discounted": discounted}
    )



def discover_your_set(request):
    
    create_set_form = CreateSetForm(request.POST)
 
    if request.method == "POST":
    
            if create_set_form.is_valid():
                cd = create_set_form.cleaned_data

                uniquesetcreation = UniqueSetCreation(

                name = cd["name"],
                surname = cd["surname"],
                birthday = cd["birthday"],
                hair_color = cd["hair_color"],
                skin_color = cd["skin_color"],
                color_tone = cd["color_tone"],
                colors_to_avoid = cd["colors_to_avoid"],
                design_preferences = cd["design_preferences"],
                overall = cd["overall_fitness"],
                individual_cut= cd["individual_cut"],
                knickers_cut =cd["knickers_cut"],
                bra_cut = cd["bra_cut"],
                activities = cd["activities"],
                preferred_details = cd["preferred_details"],
                gdpr_consent = cd["gdpr_consent"]

                )

                uniquesetcreation.save()
                try:
                    return redirect("catalog:home")
                except ssl.SSLCertVerificationError:
                    logging.info(
                        f"don't have the SSL"
                    )
                    return redirect("catalog:home")


            else:
                create_set_form = CreateSetForm()


    return render(
        request, "catalog/set_discovery.html", {"create_set_form": create_set_form}
    )


