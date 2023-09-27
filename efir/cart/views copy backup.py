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
def cart_add(request, item_id, product_id):
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


def cart_update(request, item_id):
    cart = Cart(request)

    print("tady je cart ")
    for item in cart:
        print(f"tohle to je obsah cartu, item: {item}")

    if request.method == "POST":
        item_id = request.POST.get("item_id")
        quantity = int(request.POST.get("id_quantity"))

        cart.update(item_id, quantity)  # Set add=False to directly set the quantity
        cart.save()

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)

    coupon_form = CouponForm()

    # the value is taken from session
    selected_country = request.session.get("cart_country")
    selected_address = request.session.get("cart_address")

    # the value is taken from session and saved here, where I can request it as form.initial.cart_country, etc.
    form = OrderForm(
        request.POST,
        initial={
            "order_country": selected_country,
            "order_address": selected_address,
        },
    )

    # Initialize the form without initial values

    for item in cart:
        ITEM_D = item["item_id"]
        print(f"tohle je item Id v kartu {ITEM_D}")
        product_id = item["product"].id  # Get the product ID from the item

        item["update_quantity_form"] = CartAddProductForm(
            id_from_product=product_id,
            initial={
                "quantity": item["quantity"],
                "override": True,
            },
        )

    if request.method == "POST":
        form = OrderForm(
            request.POST,
            initial={
                "order_country": selected_country,
                "order_address": selected_address,
            },
        )

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
                print("================= order is saved???")
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

    # print(form.errors)

    else:  # data has to be saved to the form, which happens
        form = OrderForm(
            request.POST,
            initial={
                "order_country": selected_country,
                "order_address": selected_address,
            },
        )

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "coupon_form": coupon_form,
            "form": form,
        },
    )


def update_cart_country(request):
    if request.method == "POST":
        selected_country = request.POST.get(
            "cart_country"
        )  # Get the selected country from the form, it has unique cart_address id and name
        selected_address = request.POST.get("cart_address")

        # Update the cart's country attribute with the selected value
        request.session["cart_country"] = selected_country

        request.session["cart_address"] = selected_address

    return redirect("cart:cart_detail")


# tyring to update through form
def update_quantity(request, product_id, item_id):
    Cart(request)

    print("update quantity request ")

    if request.method == "POST":
        # Get the item and the updated quantity from the request
        form = CartAddProductForm(id_from_product=product_id, data=request.POST)
        if form.is_valid():
            # Update the item's quantity with the new value
            item["quantity"] = form.cleaned_data["quantity"]
            # Save the updated cart item (if applicable in your model)
            item.save()
    # You can return a JsonResponse to update the quantity on the front-end

    return redirect("cart:cart_detail")
