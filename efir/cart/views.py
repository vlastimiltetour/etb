from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from catalog.models import Product
from coupons.forms import CouponForm

from .cart import Cart
from .forms import CartAddProductForm


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
                "zpusob_vyroby": item["zpusob_vyroby"],
                "override": True,
            }
        )

    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "coupon_form": coupon_form,
        },
    )