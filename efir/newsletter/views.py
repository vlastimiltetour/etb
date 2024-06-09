import logging
import ssl

from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import SubscribeForm, UnsubscribeForm
from .models import Newsletter

# Create your views here.


def subscribe_test(request):
    return render(request, "newsletter/subs_conf.html")

def unsubscribe(request):
    Newsletter.objects.all()
    unsubscribe_form = UnsubscribeForm(request.POST)


    if request.method == "POST":
        if unsubscribe_form.is_valid():

            email = unsubscribe_form.cleaned_data["email"]

            if Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.filter(email=email).delete()
                return redirect(reverse('unsubscribe'))


            else:
                return HttpResponse("Email doesn't exist")
        
    return render(request, "newsletter/unsubscribe.html", {"unsubscribe_form": unsubscribe_form})
 


def subscribe(request):
    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            # Validate reCAPTCHA
            if subscribe_form.cleaned_data.get('captcha'):
                email = subscribe_form.cleaned_data.get("email")

                if not Newsletter.objects.filter(email=email).exists():
                    Newsletter.objects.create(email=email)
                    logging.info(
                        f"Email {email} has been saved and sent subscribe confirmation"
                    )
                    try:
                        customer_order_email_confirmation(email)

                    except ssl.SSLCertVerificationError:
                        logging.info(
                            "Local environment has no email backend set up. Email: {email}"
                        )

                    return render(request, "newsletter/subs_completed.html")

                else:
                    logging.info("Email already exists in the database.")
                    return HttpResponse("Email already exists in the database.")
            else:
                return HttpResponse("reCAPTCHA validation failed")
        else:
            return HttpResponse("Form is not valid")
    else:
        subscribe_form = SubscribeForm()
    return render(request, "subscribe.html", {"subscribe_form": subscribe_form})

def customer_order_email_confirmation(email):
    # html_content = render_to_string("newsletter/subscribe.html")
    html_content = render_to_string("newsletter/subs_conf.html")
    msg = EmailMultiAlternatives(
        subject=("Děkujeme za přihlášení k odběru newsletteru od EFIR"),
        from_email="objednavky@efirthebrand.cz",
        to=[email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


"""Předmět: Děkujeme za přihlášení k odběru newsletteru od[EFIR

Dobrý den,

rádi bychom Vás srdečně přivítali v naší komunitě a poděkovali za Vaše přihlášení k odběru našeho newsletteru. Je pro nás ctí, že jste se rozhodli být součástí naší české značky ručně šitého spodního prádla EFIR the brand. 

Newsletter Vám bude posílán s osobními nabídkami, exkluzivními slevami pro naše věrné zákazníky a spoustou dalších užitečných informací, které věříme, že Vás budou potěšit. Avšak nechceme Vás otravovat a budeme posílat pouze relevantní a přínosné informace.

Pokud byste měli jakékoliv dotazy, připomínky nebo náměty, neváhejte nás kontaktovat. Jsme tu pro Vás.

Děkujeme Vám ještě jednou za Vaši důvěru a těšíme se na naši budoucí spolupráci.

S pozdravem,

Valérie

Majitelka a hlavní návrhářka 
EFIR the brand"""


"""ion", [])
    size_selection_session = request.session.get("size_selection_session", [])
    sort_by_price_session = request.session.get("sort_by_price_session", "created")
    cut_selection_session = request.session.get("cut_selection_session", [])
    category_session = request.session.get("category_session", [])

    # these are session contents
    # print(show_session_contents(request))

    query_filters = Q()

    if category_session:
        query_filters &= Q(category__name=category_session[0])

    if cut_selection_session:
        if type(cut_selection_session) == str:
            if cut_selection_session == "Brazilky":
                # Filter for products containing "Brazilky" but exclude those containing "Brazilky na gumičkách"
                query_filters &= Q(short_description__icontains="Brazilky")
                query_filters &= ~Q(
                    short_description__icontains="Brazilky na gumičkách"
                )
            elif cut_selection_session == "Podprsenka s kosticemi":
                # Filter for products containing "Brazilky" but exclude those containing "Brazilky na gumičkách"
                query_filters &= Q(
                    short_description__icontains="Podprsenka s kosticemi"
                )
                query_filters &= ~Q(
                    short_description__icontains="Podprsenka s kosticemi a otevřeným košíčkem"
                )

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
        products = (
            Product.objects.filter(query_filters)
            .order_by(sort_by_price_session)
            .filter(active=True)
        )

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

        for session_key, session_value in request.session.items():
            if isinstance(session_value, (list, str)):
                if selected_filter in session_value:
                    print("session_key", session_key)
                    print("selected filter:", selected_filter)

        del request.session[session_key]

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
    products = Product.objects.all().filter(active=True)
    discounted = Product.objects.exclude(discount__isnull=True).filter(active=True)

    print("these are akce discounts:", discounted)

    return render(
        request, "catalog/akce.html", {"products": products, "discounted": discounted}
    )


def discover_your_set(request):
    create_set_form = CreateSetForm(request.POST)
    print(create_set_form.errors)
    if request.method == "POST":
        if create_set_form.is_valid():
            cd = create_set_form.cleaned_data

            uniquesetcreation = UniqueSetCreation(
                name=cd["name"],
                surname=cd["surname"],
                birthday=cd["birthday"],
                hair_color=cd["hair_color"],
                skin_color=cd["skin_color"],
                color_tone=cd["color_tone"],
                colors_to_avoid=cd["colors_to_avoid"],
                design_preferences=cd["design_preferences"],
                overall=cd["overall_fitness"],
                individual_cut=cd["individual_cut"],
                knickers_cut=cd["knickers_cut"],
                bra_cut=cd["bra_cut"],
                activities=cd["activities"],
                preferred_details=cd["preferred_details"],
                gdpr_consent=cd["gdpr_consent"],
            )
            print(create_set_form.errors)
            uniquesetcreation.save()
            try:
                return render(
                    request,
                    "catalog/set_discovery_completed.html",
                    {"create_set_form": create_set_form},
                )
            except ssl.SSLCertVerificationError:
                logging.info("don't have the SSL")
                return render(
                    request,
                    "catalog/set_discovery_completed.html",
                    {"create_set_form": create_set_form},
                )

        else:
            print(create_set_form.errors)
            create_set_form = CreateSetForm()

    print(create_set_form.errors)
    return render(
        request, "catalog/set_discovery.html", {"create_set_form": create_set_form}
    )


def objednat_na_miru(request):
    categories = Category.objects.all()
    mapping_siti_na_miru_form = MappingSetNaMiruForm(request.POST)
    print(mapping_siti_na_miru_form.errors)

    if request.method == "POST":
        if mapping_siti_na_miru_form.is_valid():
            cd = mapping_siti_na_miru_form.cleaned_data

            mappingsetnamiru = MappingSetNaMiru(
                name=cd["name"],
                surname=cd["surname"],
                email=cd["email"],
                number=cd["number"],
                set_selection=cd["set_selection"],
                gdpr_consent=cd["gdpr_consent"],
                newsletter_consent=cd["newsletter_consent"],
            )
            mappingsetnamiru.save()

            mapping_id = mappingsetnamiru.id
            siti_na_miru_email_confirmation(mapping_id)

            try:
                return render(
                    request,
                    "catalog/set_discovery_completed.html",
                    {"mappingsetnamiru": mappingsetnamiru},
                )
            except ssl.SSLCertVerificationError:
                logging.info("don't have the SSL, but the email has been sent")
                return render(
                    request,
                    "catalog/set_discovery_completed.html",
                    {"mappingsetnamiru": mappingsetnamiru},
                )

        else:
            print(mappingsetnamiru.errors)
            mappingsetnamiru = MappingSetNaMiruForm()

    return render(
        request,
        "catalog/na_miru.html",
        {
            "categories": categories,
            "mapping_siti_na_miru_form": mapping_siti_na_miru_form,
        },
    )
"""
