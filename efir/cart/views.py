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
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            obvod_hrudnik=cd["obvod_hrudnik"],
            obvod_prsa=cd["obvod_prsa"],
            obvod_boky=cd["obvod_boky"],
            zpusob_vyroby=cd["zpusob_vyroby"],
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
        item["update_quantity_form"] = CartAddProductForm(
            initial={
                "quantity": item["quantity"],
                "obvod_prsa": item["obvod_prsa"],
                "obvod_hrudnik": item["obvod_hrudnik"],
                # translates from cart_product_form to cart detail specifically with {{ item.update_quantity_form }}
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
