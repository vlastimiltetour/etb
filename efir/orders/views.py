import logging
import ssl

from django.shortcuts import get_object_or_404, render

from cart.cart import Cart

from .forms import OrderForm
from .mail_confirmation import *
from .models import Order, OrderItem

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)


def new_order(request):
    cart = Cart(request)

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                )
            # clear the cart
            cart.clear()
            order_id = order.id

            customer_order_email_confirmation(order_id)

            '''try:
                customer_order_email_confirmation(order_id)
            except ssl.SSLCertVerificationError:
                logging.info(f"Local environment has no email sending{order_id}")'''

            return render(request, "orders/objednavka_vytvorena.html", {"order": order})
    else:
        form = OrderForm()

    return render(request, "orders/new.html", {"cart": cart, "form": form})


def objednavka_vytvorena(request):
    id = 2
    order = get_object_or_404(Order, id=id)
    return render(request, "orders/objednavka_vytvorena.html", {"order": order})
