import random
import string
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from orders.models import OrderItem

from .forms import CouponForm
from .models import Coupon


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data["code"]
        print(code)
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True
            )
            if coupon.capacity > 0:
                request.session["coupon_id"] = coupon.id

        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None

    return redirect("cart:cart_detail")


def coupon_delete(request):
    request.session["coupon_id"]
    request.session["coupon_id"] = None

    return redirect("cart:cart_detail")


def coupon_deactivate(request):
    coupon_id = request.session["coupon_id"]
    print(coupon_id)

    try:
        coupon = get_object_or_404(Coupon, id=coupon_id)

        # Set the coupon's 'active' field to False
        coupon.capacity -= 1
        if coupon.capacity == 0:
            coupon.active = False
            coupon.redeemed = True

        coupon.save()

        # Remove the coupon_id from the session
    except TypeError:
        request.session["coupon_id"] = coupon.id

    except KeyError:
        return redirect("cart:cart_detail")

    request.session["coupon_id"] = None

    return redirect("cart:cart_detail")


def coupon_create(
    request,
    discount_value,
    discount_type,
    discount_threshold,
    category,
    id,
    orderitem_id,
    certificate_from,
    certificate_to,
):
    code = generate_voucher_code(8)
    valid_from = datetime.now()
    valid_to = valid_from + timedelta(days=180)
    print(f"this is coupon create function, and this is discount {discount_value}")
    active = True
    redeemed = False

    if discount_type == "Procento":
        discount_value = discount_value / 100

    coupon = Coupon.objects.create(
        code=code,
        valid_from=valid_from,
        valid_to=valid_to,
        discount_value=discount_value,
        discount_threshold=discount_threshold,
        discount_type=discount_type,
        category=category,
        active=active,
        redeemed=redeemed,
        order_id=id,
        certificate_from=certificate_from,
        certificate_to=certificate_to,
    )

    try:
        product_orderitem = OrderItem.objects.get(id=orderitem_id)
        product_orderitem.slevovy_kod = coupon.code
        product_orderitem.hodnota_kuponu = coupon.discount_value
        product_orderitem.save()
    except OrderItem.DoesNotExist:
        # Handle the case where the OrderItem does not exist
        product_orderitem = None  # Or any default value or action you want to take

    # Storing coupon_id in session
    # request.session["newly_created_coupon_id"] = coupon_id
    # request.session.save()

    return HttpResponse(f"Coupon created successfully! {coupon}")


def generate_voucher_code(length):
    characters = (
        string.ascii_uppercase + string.digits
    )  # Use uppercase letters and numbers
    voucher_code = "".join(random.choice(characters) for _ in range(length))
    return voucher_code


def generate_vouchers_X(request):
    for i in range(200):
        coupon_create(
            request,
            id=0,
            orderitem_id=0,
            category="Sleva na první nákup",
            discount_value=300,
            discount_type="Částka",
            discount_threshold=1,
            certificate_from="-",
            certificate_to="-",
        )

    for i in range(200):
        coupon_create(
            request,
            id=0,
            orderitem_id=0,
            category="Odměna 30 dní po 1. nákupu",
            discount_value=10,
            discount_type="Procento",
            discount_threshold=1,
            certificate_from="-",
            certificate_to="-",
        )

    for i in range(200):
        coupon_create(
            request,
            id=0,
            orderitem_id=0,
            category="Sleva po 3 měsících",
            discount_value=10,
            discount_type="Procento",
            discount_threshold=1,
            certificate_from="-",
            certificate_to="-",
        )

    for i in range(300):
        coupon_create(
            request,
            id=0,
            orderitem_id=0,
            category="Přání k svátku",
            discount_value=15,
            discount_type="Procento",
            discount_threshold=1,
            certificate_from="-",
            certificate_to="-",
        )

    return HttpResponse("Vouchers have been created")


from datetime import datetime

from django.db import transaction

from .models import Coupon


def generate_vouchers(request):
    coupons_data = [
        {
            "code": "252FZ6TO",
            "order_id": "24062012",
            "valid_from": "2024-06-20",
            "valid_to": "2024-12-17",
            "discount_type": "Částka",
        },
        {
            "code": "2YZH2N5D",
            "order_id": "24062000",
            "valid_from": "2024-06-20",
            "valid_to": "2024-12-17",
            "discount_type": "Částka",
        },
        {
            "code": "LUCIE20",
            "order_id": "N/A",
            "valid_from": "2024-06-11",
            "valid_to": "2024-12-11",
            "discount_type": "Procento",
        },
        {
            "code": "9SS6XAKA",
            "order_id": "24061003",
            "valid_from": "2024-06-10",
            "valid_to": "2024-12-07",
            "discount_type": "Částka",
        },
        {
            "code": "KLARA",
            "order_id": "N/A",
            "valid_from": "2024-06-10",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "TEREZA",
            "order_id": "N/A",
            "valid_from": "2024-05-31",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "ROZA",
            "order_id": "N/A",
            "valid_from": "2024-05-26",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "NADYA",
            "order_id": "N/A",
            "valid_from": "2024-05-26",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "ANASTASIA",
            "order_id": "N/A",
            "valid_from": "2024-05-26",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "KSENIA",
            "order_id": "N/A",
            "valid_from": "2024-05-26",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "DARIA",
            "order_id": "N/A",
            "valid_from": "2024-05-26",
            "valid_to": "2024-12-31",
            "discount_type": "Procento",
        },
        {
            "code": "KATUS15",
            "order_id": "N/A",
            "valid_from": "2024-06-01",
            "valid_to": "2024-06-01",
            "discount_type": "Procento",
        },
        {
            "code": "ADRI15",
            "order_id": "N/A",
            "valid_from": "2024-05-24",
            "valid_to": "2024-06-03",
            "discount_type": "Procento",
        },
        {
            "code": "5VERZAK342",
            "order_id": "N/A",
            "valid_from": "2024-05-19",
            "valid_to": "2024-05-23",
            "discount_type": "Částka",
        },
    ]

    with transaction.atomic():
        for data in coupons_data:
            coupon, created = Coupon.objects.get_or_create(
                code=data["code"],
                defaults={
                    "valid_from": datetime.strptime(
                        data["valid_from"], "%Y-%m-%d"
                    ).date(),
                    "valid_to": datetime.strptime(data["valid_to"], "%Y-%m-%d").date(),
                    "discount_type": data["discount_type"],
                    "discount_threshold": 1,
                    "certificate_from": "-",
                    "certificate_to": "-",
                    "category": "-",
                    "order_id": data["order_id"],
                    "active": True,
                },
            )
            if not created:
                # Handle cases where the coupon already exists
                pass

    return HttpResponse("Vouchers have been created")
