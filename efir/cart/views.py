import logging
from decimal import Decimal

from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from cart.cart import Cart
from catalog.models import Certificate, Product
from coupons.forms import Coupon, CouponForm
from coupons.views import coupon_create, coupon_deactivate
from inventory.models import Inventory
from orders.forms import OrderForm
from orders.mail_confirmation import *
from orders.models import OrderItem

logger = logging.getLogger(__name__)

from .cart import Cart
from .forms import CartAddProductForm

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)


from django.http import HttpResponseBadRequest


@require_POST
def cart_add(request, product_id):
    inventory_capacity = False
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(id_from_product=product_id, data=request.POST)
    inventory = Inventory.objects.filter(product=product).first()
    Certificate.objects.filter(product=product).first()

    if form.is_valid():
        form.set_cart_values()
        cd = form.cleaned_data

        if inventory_capacity:
            if cd["quantity"] > inventory.quantity:
                form.add_error("quantity", "Quantity exceeds available inventory")
                return HttpResponseBadRequest(
                    "Zvolený počet daného produktu přesahuje kapacitu skladu."
                )

        cart.add(
            product=product,
            quantity=cd["quantity"],
            poznamka=cd["poznamka"],
            velikost=cd["velikost"],
            kalhotky_velikost_set=cd["kalhotky_velikost_set"],
            podprsenka_velikost_set=cd["podprsenka_velikost_set"],
            pas_velikost_set=cd["pas_velikost_set"],
            zpusob_vyroby=cd["zpusob_vyroby"],
            override=cd["override"],
            certificate_from=cd["certificate_from"],
            certificate_to=cd["certificate_to"],
        )
        zpusob_vyroby = cd["zpusob_vyroby"]
        print("this is the form add to cart", {form})

        if str(product.category) == "Dárkové certifikáty":
            print("produkt jsou darkove certifikaty jo")
            if zpusob_vyroby == "Elektronický":
                print("ano zpusob vyroby je elektronicky")
                update_cart_country(request, online=True)
            else:
                print("ne zpusob vyroby nefunguje")
        else:
            update_cart_country(request, online=False)

    else:
        print(form.errors)

    # return JsonResponse({'success': True})

    # return redirect("cart:cart_detail")
    return redirect("catalog:product_detail", id=product_id, slug=product.slug)

    # return reverse("product_detail", request, id=2, slug='hello')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    # messages.info(request, f"{product.name} has been removed from your cart.")

    return redirect("cart:cart_detail")


def update_cart_quantity(request, item_id):
    new_quantity = int(request.POST["quantity"])
    cart = Cart(request)
    cart.update_quantity(item_id, new_quantity)
    return redirect("cart:cart_detail")


def cart_detail(request, zasilkovna=True):
    certificate = 0
    try:
        cart = Cart(request)
        for item in cart:
            print(f"this is the cart contents, item: {item}")

        # Rest of your view logic

    except TypeError as e:
        logger.error(f"An error occurred in the cart_detail view: {e}")
        clean_cart_session(request)

    cart = Cart(request)
    coupon_form = CouponForm()

    # the value is taken from session
    selected_country = request.session.get("cart_country")
    selected_address = request.session.get("cart_address")
    selected_vendor_id = request.session.get("cart_vendor")
    selected_cart_shipping = request.session.get("cart_shipping")
    selected_cart_city = request.session.get("cart_city")
    selected_cart_zipcode = request.session.get("cart_zipcode")

    selected_certificate_shipping = request.session.get("zpusob_vyroby")
    print("this is selectedcertiiccate online", selected_certificate_shipping)

    for key, value in request.session.items():
        if isinstance(value, Decimal):
            value = str(value)
        print(f"Key: {key}, Value: {value}, type{type(value)}")

    if cart.get_shipping_price() == 0:
        print("cena se rovna nule")
        update_cart_country(request, online=True)

    # the value is taken from session and saved here, where I can request it as form.initial.cart_country, etc.
    form = OrderForm(
        request.POST,
        initial={
            "order_country": selected_country,
            "order_address": selected_address,
            "vendor_id": selected_vendor_id,
            "order_shipping": selected_cart_shipping,
            "order_city": selected_cart_city,
            "order_zipcode": selected_cart_zipcode,
        },
    )
    # print("Form data:", form.data)

    # Initialize the form without initial values

    for item in cart:
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
                "vendor_id": selected_vendor_id,
                "order_shipping": selected_cart_shipping,
                "order_city": selected_cart_city,
                "order_zipcode": selected_cart_zipcode,
            },
        )

        if form.is_valid():
            # print("form contents", form)
            order = form.save(
                commit=False
            )  # In this line, you are using a Django ModelForm (order_form) to create an Order instance. The commit=False argument prevents the instance from being saved to the database immediately. Instead, it returns an unsaved instance of the model. This allows you to make additional modifications to the instance before saving it to the database.

            order.save(cart=cart)
            order.city = selected_cart_city

            order.zipcode = selected_cart_zipcode
            order.shipping_price = cart.get_shipping_price()
            print("this is shiping price:", cart.get_shipping_price())
            order.save()
            print("thse are order contents", order)

            """Once you have the unsaved order instance, you can call its save method to save it to the database. In this case, you are passing an additional keyword argument cart to the save method. This is where you are providing the cart instance to the save method of the Order model.
            In the save method of the Order model, you are accessing the cart instance through this passed keyword argument to calculate the total_cost for the order. This is a way to pass contextual information from the view (the cart instance) to the model (Order instance) when saving it.
            The combination of these lines ensures that the Order instance is created from the form data but not immediately saved, allowing you to calculate and set additional fields like total_cost before the final save."""

            for item in cart:
                # I'd create if item.product.cateogory == "Darkove certifikaty"
                # Your existing code for processing cart items
                if item["product"].category.name == "Dárkové certifikáty":
                    for i in range(item["quantity"]):
                        print("this is round", {i})
                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            price=item["price"],
                            total_price=item["total_price"],
                            surcharge=item["surcharge"],
                            quantity=1,
                            zpusob_vyroby=item["zpusob_vyroby"],
                            velikost=item["velikost"],
                            kalhotky_velikost_set=item["kalhotky_velikost_set"],
                            podprsenka_velikost_set=item["podprsenka_velikost_set"],
                            pas_velikost_set=item["pas_velikost_set"],
                            poznamka=item["poznamka"],
                            certificate_from=item["certificate_from"],
                            certificate_to=item["certificate_to"],
                        )

                else:
                    OrderItem.objects.create(
                        order=order,
                        product=item["product"],
                        price=item["price"],
                        total_price=item["total_price"],
                        surcharge=item["surcharge"],
                        quantity=item["quantity"],
                        zpusob_vyroby=item["zpusob_vyroby"],
                        velikost=item["velikost"],
                        kalhotky_velikost_set=item["kalhotky_velikost_set"],
                        podprsenka_velikost_set=item["podprsenka_velikost_set"],
                        pas_velikost_set=item["pas_velikost_set"],
                        poznamka=item["poznamka"],
                        certificate_from=item["certificate_from"],
                        certificate_to=item["certificate_to"],
                    )

            order_items = OrderItem.objects.filter(order=order)

            request.session["order_id"] = order.id

            order_id = order.id
            print(
                "order has been created under",
                {order_id},
                "and order_items",
                {order_items},
            )

            for order_item in order_items:
                item_product = order_item.product

                # conditions to check for discount
                # this to be repaierd
                if str(item_product.category) == "Dárkové certifikáty":
                    # coupon_create(request, certificate_discount)
                    print(" coupn create should have happened")
                    discount_value = item_product.certificate.discount_value
                    discount_type = item_product.certificate.discount_type
                    discount_treshold = item_product.certificate.discount_threshold
                    certificate_category = "Dárkový certifikát"
                    print("this is order_item id", order_item.id)
                    ##rekl bych ze sem nekam ten coupon
                    print("this is order_item check 1", order_item, order_item.quantity)

                    for i in range(order_item.quantity):
                        print(
                            "this is order_item check 2",
                            order_item,
                            order_item.quantity,
                        )
                        coupon_create(
                            request.GET,
                            discount_value,
                            discount_type,
                            discount_treshold,
                            category=certificate_category,
                            id=order.etb_id,
                            orderitem_id=order_item.id,
                            certificate_from=order_item.certificate_from,
                            certificate_to=order_item.certificate_to,
                        )

                # this is inventory solution
                """size = order_item.velikost
                quantity = order_item.quantity

                
                try:
                    inventory = Inventory.objects.get(product=product, size=size)
                    inventory.quantity -= quantity
                    inventory.save()

                except IntegrityError as e:
                    # Handle the specific IntegrityError related to the CHECK constraint
                    print(f"IntegrityError: {e}. Not enough items to sell.")
                    # You might want to log the error or take appropriate action
                    return redirect("cart:cart_detail")

                except Inventory.DoesNotExist:
                    # Handle the case where the inventory record does not exist
                    print(
                        f"Inventory record not found for product {product} and size {size}"
                    )
                    return redirect("cart:cart_detail")"""

            # coupon apply - saving the applyed coupon code discount into the order
            try:
                coupon_id = request.session["coupon_id"]
                coupon = Coupon.objects.get(id=coupon_id)
                coupon_code = coupon.code
                order.discount_code = coupon_code
                order.save()
                coupon_deactivate(request)
            except KeyError:
                print("Coupon not found for ID -, no coupon applied")
            except Coupon.DoesNotExist:
                print("Coupon not found for ID, no coupon applied")

            cart.clear()
            # return render(request, "orders/objednavka_vytvorena.html", {"order": order})

            return redirect(reverse("stripepayment:process"))

        print(form.errors)

    else:  # data has to be saved to the form, and if the form is reastarted, it's brought back again here
        form = OrderForm(
            request.POST,
            initial={
                "order_country": selected_country,
                "order_address": selected_address,
                "vendor_id": selected_vendor_id,
                "order_shipping": selected_cart_shipping,
                "order_city": selected_cart_city,
                "order_zipcode": selected_cart_zipcode,
            },
        )

    print("overuji hodnotu cetifitkatu", certificate)
    return render(
        request,
        "cart/cart.html",
        {
            "cart": cart,
            "coupon_form": coupon_form,
            "form": form,
            "certificate": certificate,
        },
    )


def update_cart_country(request, online=None):
    print("update cart country has been triggered")
    if online:
        if request.method == "POST":
            selected_country = request.POST.get(
                "cart_country"
            )  # Get the selected country from the form, it has unique cart_address id and name
            selected_address = request.POST.get("cart_address")
            selected_vendor_id = request.POST.get("cart_vendor")
            selected_cart_shipping = request.POST.get("cart_shipping")
            selected_cart_city = request.POST.get("cart_city")
            selected_cart_zipcode = request.POST.get("cart_zipcode")

            # Update the cart's country attribute with the selected value

            request.session["cart_country"] = "online"
            request.session["cart_address"] = "online"
            request.session["cart_vendor"] = "-"
            request.session["cart_shipping"] = "O"
            request.session["cart_city"] = ""
            request.session["cart_zipcode"] = ""
            # request.save()

    else:
        if request.method == "POST":
            selected_country = request.POST.get(
                "cart_country"
            )  # Get the selected country from the form, it has unique cart_address id and name
            selected_address = request.POST.get("cart_address")
            selected_vendor_id = request.POST.get("cart_vendor")
            selected_cart_shipping = request.POST.get("cart_shipping")
            selected_cart_city = request.POST.get("cart_city")
            selected_cart_zipcode = request.POST.get("cart_zipcode")

            # Update the cart's country attribute with the selected value

            request.session["cart_country"] = selected_country
            request.session["cart_address"] = selected_address
            request.session["cart_vendor"] = selected_vendor_id
            request.session["cart_shipping"] = selected_cart_shipping
            request.session["cart_city"] = selected_cart_city
            request.session["cart_zipcode"] = selected_cart_zipcode
            # request.save()

    return redirect("cart:cart_detail")


def set_cart_online(request):
    print("jo stoji to nuul")
    for session_key, session_value in request.session.items():
        if isinstance(session_value, (list, str)):
            if "cart_vendor" in session_value:
                print("session_key", session_key)
                print("selected filter:", session_value)
                request.session["cart_vendor"] = "-"

    return redirect("cart:cart_detail")


def clean_cart_session(request):
    cart = Cart(request)
    cart.clean_cart_session()
    return redirect("catalog:home")
