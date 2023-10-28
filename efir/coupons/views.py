import random
import string
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import CouponForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            request.session["coupon_id"] = coupon.id

        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None
    return redirect("cart:cart_detail")


def coupon_deactivate(request):
    try:
        coupon_id = request.session["coupon_id"]
        coupon = get_object_or_404(Coupon, id=coupon_id)

        # Set the coupon's 'active' field to False
        coupon.active = False
        coupon.redeemed = True
        coupon.save()

        # Remove the coupon_id from the session
        request.session["coupon_id"] = None
    except KeyError:
        return redirect("cart:cart_detail")

    return redirect("cart:cart_detail")


def coupon_create(request, discount):
    code = generate_voucher_code(8)
    valid_from = datetime.now()
    valid_to = valid_from + timedelta(days=180)
    discount = discount
    print(f"this is coupon create function, and this is discount {discount}")
    active = True
    redeemed = False

    coupon = Coupon.objects.create(
        code=code,
        valid_from=valid_from,
        valid_to=valid_to,
        discount=discount,
        active=active,
        redeemed=redeemed,
    )

    print(f"this is the newly created voucher code! {coupon}")

    return HttpResponse(f"Coupon created successfully! {coupon}")


def generate_voucher_code(length):
    characters = (
        string.ascii_uppercase + string.digits
    )  # Use uppercase letters and numbers
    voucher_code = "".join(random.choice(characters) for _ in range(length))
    return voucher_code
