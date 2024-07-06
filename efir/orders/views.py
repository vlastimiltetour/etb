import logging
import mimetypes
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .mail_confirmation import *
from .models import Order

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

""


# todo this can be deleted
def new_order(request):
    pass
    ''' cart = Cart(request)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(
                commit=False
            )  # In this line, you are using a Django ModelForm (order_form) to create an Order instance. The commit=False argument prevents the instance from being saved to the database immediately. Instead, it returns an unsaved instance of the model. This allows you to make additional modifications to the instance before saving it to the database.
            order.save(cart=cart)
            """Once you have the unsaved order instance, you can call its save method to save it to the database. In this case, you are passing an additional keyword argument cart to the save method. This is where you are providing the cart instance to the save method of the Order model.
            In the save method of the Order model, you are accessing the cart instance through this passed keyword argument to calculate the total_cost for the order. This is a way to pass contextual information from the view (the cart instance) to the model (Order instance) when saving it.
            The combination of these lines ensures that the Order instance is created from the form data but not immediately saved, allowing you to calculate and set additional fields like total_cost before the final save."""

            order_form_data = {
                "order_id": order.id,
                "country": order.country,
                # Add any other data you want to include here...
            }

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                    velikost=item["velikost"],
                )

            # clear the cart

            cart.clear()

            request.session["order_id"] = order.id

            try:
                order_id = order.id
                zasilkovna_create_package(order_id)
                customer_order_email_confirmation(order_id)

            except ssl.SSLCertVerificationError:
                logging.info(
                    f"Local environment has no email backend set up.Order ID: {order_id}"
                )

            # return render(request, "orders/objednavka_vytvorena.html", {"order": order})
            return redirect(reverse("stripepayment:process"))
    else:
        form = OrderForm()

    return render(
        request,
        "orders/new.html",
        {"cart": cart, "form": form, order_form_data: "order_form_data"},
    )
'''


def calculate_shipping_price(country_code):
    if country_code == "CZ":
        return 79
    elif country_code == "SK":
        return 89
    elif country_code == "EK":
        return 0
    else:
        return 0
    # Add other country prices here


def invoice(request):
    id = 413
    order = get_object_or_404(Order, id=id)
    print(order)
    return render(request, "orders/invoice_pdf.html", {"order": order})



    order = get_object_or_404(Order, id=id)

    print(order)
    return render(request, "orders/certificate_confirmation.html", {"order": order})

def update_orders(request):
    selected_order = Order.objects.filter(id=939)
    selected_order.update(discount=-300, total_cost=2029)
    return HttpResponse("Order has been corrected")

def contact_form(request):
    return render(request, "orders/contact_form.html")


def download_ppl_label(request, file_name):
    # file_path = "media/assets/Reklamace.pdf"  # URL to your file

    file_path = os.path.join(
        settings.MEDIA_ROOT, "catalog/ppl_labels", file_name + ".pdf"
    )
    fl = open(file_path, "rb")
    mime_type, _ = mimetypes.guess_type(file_path)
    response = HttpResponse(fl, content_type=mime_type)
    response["Content-Disposition"] = "attachment; filename=%s" % file_name
    return response
