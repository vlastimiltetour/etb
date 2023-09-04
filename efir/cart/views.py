import logging
import ssl

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from cart.cart import Cart
from catalog.models import Product
from coupons.forms import CouponForm
from orders.forms import OrderForm
from orders.mail_confirmation import *
from orders.models import OrderItem
from stripepayment.views import zasilkovna_create_package

from .cart import Cart
from .forms import CartAddProductForm

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(id_from_product=product_id, data=request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            obvod_hrudnik=cd["obvod_hrudnik"],
            obvod_prsa=cd["obvod_prsa"],
            obvod_boky=cd["obvod_boky"],
            obvod_body=cd["obvod_body"],
            zpusob_vyroby=cd["zpusob_vyroby"],
            poznamka=cd["poznamka"],
            override=cd["override"],
        )

    return redirect("cart:cart_detail")


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)

    coupon_form = CouponForm()

    for item in cart:
        product_id = item["product"].id  # Get the product ID from the item
        item["update_quantity_form"] = CartAddProductForm(
            id_from_product=product_id,
            initial={
                "quantity": item["quantity"],
                "obvod_prsa": item["obvod_prsa"],
                "obvod_hrudnik": item["obvod_hrudnik"],
                "obvod_boky": item["obvod_boky"],
                "obvod_body": item["obvod_body"],
                "zpusob_vyroby": item["zpusob_vyroby"],
                "override": True,
            },
        )

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

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    price=item["price"],
                    quantity=item["quantity"],
                    zpusob_vyroby=item["zpusob_vyroby"],
                    obvod_hrudnik=item["obvod_hrudnik"],
                    obvod_prsa=item["obvod_prsa"],
                    obvod_boky=item["obvod_boky"],
                    obvod_body=item["obvod_body"],
                )
                print("order is saved???")
                print(f"orderitem{order}")
                print(f"item{item}")

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
        "cart/cart.html",
        {
            "cart": cart,
            "coupon_form": coupon_form,
            "form": form,
        },
    )
