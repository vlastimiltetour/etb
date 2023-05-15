from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.cart import Cart
from cart.forms import CartAddProductForm
from catalog.models import Product

from .forms import OrderForm
from .mail_confirmation import *
from .models import Order, OrderItem


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
            order_email_confirmation(order_id)

            return render(request, "orders/objednavka_vytvorena.html", {"order": order})

    else:
        form = OrderForm()
    return render(request, "orders/new.html", {"cart": cart, "form": form})


def objednavka_vytvorena(request):
    id = 71
    order = get_object_or_404(Order, id=id)
    # order_email_confirmation(id)
    order_email_confirmation(id)
    send_email()
    return render(request, "orders/objednavka_vytvorena.html", {"order": order})
