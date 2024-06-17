import json
import logging
import time
from decimal import Decimal

import requests
import stripe
import unidecode
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from efir.settings.base import ZASILKOVNA_SECRET
from orders.models import Order, OrderItem

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

import logging
import smtplib
import ssl
import xml.etree.ElementTree as ET
from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from cart.cart import Cart
from coupons.forms import Coupon
from orders.mail_confirmation import *

logger = logging.getLogger(__name__)

from cart.cart import Cart

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)


def payment_process(request):
    order_id = request.session.get("order_id")
    # order_id = 4

    order = get_object_or_404(Order, id=order_id)

    payment_attempts = request.session.get("payment_attempts", 0)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("stripepayment:completed"))
        cancel_url = request.build_absolute_uri(reverse("stripepayment:canceled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.etb_id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        # Add order items to the Stripe checkout session, this is going to loop over the data structure
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(order.total_cost * Decimal("100")),
                        "currency": "czk",
                        "product_data": {
                            "name": f"Objednavka cislo {order.etb_id}",
                        },
                    },
                    "quantity": 1,
                },
            )
            # but as the price is given from order.total_cost, I break the loop sooner
            break

        # Create Stripe checkout session

        # Redirect to Stripe payment form
        try:
            checkout_session = stripe.checkout.Session.create(**session_data)
            return redirect(checkout_session.url)
        except stripe.error.InvalidRequestError:
            payment_attempts += 1

            request.session["payment_attempts"] = payment_attempts

            # If there have been three unsuccessful attempts, cancel the transaction
            if payment_attempts >= 3:
                return redirect(reverse("stripepayment:canceled"))
            else:
                # If there's an error in creating the checkout session,
                # redirect back to the payment process page to retry
                # return redirect(reverse("stripepayment:payment_process"))
                pass
    # else:
    return render(request, "stripe/process.html", locals())


def zasilkovna_create_package(order_id):
    # order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    api_password = ZASILKOVNA_SECRET
    endpoint = "https://www.zasilkovna.cz/api/rest"
    order_id = str(order.etb_id)
    order_name = order.first_name
    order_surname = order.last_name
    order_email = order.email
    vendor_id = order.vendor_id
    order_price = str(order.total_cost)
    weight = "0.5"  # set up
    currency = "CZK"

    order_name = unidecode.unidecode(order_name)
    order_surname = unidecode.unidecode(order_surname)
    # Create a dictionary representing the order details
    order_details = {
        "apiPassword": api_password,
        "packetAttributes": {
            "number": order_id,
            "name": order_name,
            "surname": order_surname,
            "email": order_email,
            "addressId": vendor_id,
            "currency": currency,
            "value": order_price,
            "weight": weight,
            "eshop": "efirthebrand.cz",
        },
    }

    print(f"vendor_id {order.vendor_id}")
    print(f"address id: {order_details}")

    # Convert the dictionary to XML
    root = ET.Element("createPacket")
    api_password_elem = ET.SubElement(root, "apiPassword")
    api_password_elem.text = api_password

    packet_attributes_elem = ET.SubElement(root, "packetAttributes")

    for key, value in order_details["packetAttributes"].items():
        elem = ET.SubElement(packet_attributes_elem, key)
        elem.text = value

    xml_data = ET.tostring(root, encoding="unicode")

    headers = {"Content-Type": "application/xml"}

    # print((endpoint, xml_data, headers))

    print(xml_data)
    # download_label(request, order_id)

    # <response><status>ok</status><result><id>1898524069</id><barcode>Z1898524069</barcode><barcodeText>Z 189 8524 069</barcodeText></result></response>

    response = requests.post(endpoint, data=xml_data, headers=headers)

    if response.status_code == 200:
        print("Order created successfully!")
        print("Response Content:")
        print(response.content)

        try:
            xml_response = response.content
            root = ET.fromstring(xml_response)
            status_text = root.find("status").text
            packet_id = root.find("result/id").text
            barcode_text = root.find("result/barcodeText").text

            print(f"Status: {status_text}")
            print(f"Packet ID: {packet_id}")
            print(f"Barcode Text: {barcode_text}")

            # packetLabelPdf(packetId=packet_id, format="A7 on A4", offset=0)
        except AttributeError as e:
            print("An error occurred while parsing the XML response:", e)


from django.http import HttpResponse


def packetLabelPdf(packetId, format="A7 on A4", offset=0):
    packetId = 2336806921
    api_password = ZASILKOVNA_SECRET
    endpoint = "https://www.zasilkovna.cz/api/rest"
    xml_data = f"""
    <packetLabelPdf>
        <apiPassword>{api_password}</apiPassword>
        <packetId>{packetId}</packetId>
        <format>{format}</format>
        <offset>{offset}</offset>
    </packetLabelPdf>
    """

    headers = {"Content-Type": "application/xml"}
    response = requests.post(endpoint, data=xml_data, headers=headers)

    pdf_content = response.content

    # Create an HTTP response with the PDF content
    pdf_response = HttpResponse(pdf_content, content_type="application/pdf")
    pdf_response["Content-Disposition"] = 'inline; filename="packet_label.pdf"'

    # Assuming Zasilkovna API returns XML data
    xml_content = response.content

    # Create an HTTP response with the XML content
    xml_response = HttpResponse(xml_content, content_type="application/xml")
    xml_response["Content-Disposition"] = 'attachment; filename="packet_label.xml"'

    return pdf_response


def payment_notification(request):
    if request.method == "POST":
        # Get the notification data from the request
        try:
            notification_data = json.loads(request.body)
            notification_data.get("orderId")
            notification_data.get("status")

            # Update the order status in your database based on the received data
            # Example: Update the order status for orderId in your database

            # ... your code to update the order status in the database goes here ...

            return HttpResponse(status=200)  # Return success status
        except json.JSONDecodeError as e:
            # Handle JSON decoding error
            return HttpResponse(status=400, content=f"JSON decoding error: {str(e)}")
        except Exception as e:
            # Handle other exceptions
            return HttpResponse(status=500, content=f"Error occurred: {str(e)}")
    else:
        return HttpResponse(status=405)  # Method not allowed for other request types


def payment_completed(request):
    order_id = request.session.get("order_id")
    # order_id = 364
    cart = Cart(request)
    certificate = False
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order)

    """for order_item in order_items:
        print(order_item.product.name)
        if (str(order_item.product.category)) == "Dárkové certifikáty":   
            certificate = True     """
    certificate = any(
        str(order_item.product.category) == "Dárkové certifikáty"
        for order_item in order_items
    )
    print("tady se snazim vytisknout certificate", certificate)

    try:
        if certificate is True:
            print("ANO ANO ANO YES posli potvzrni certifikatu")
            certificate_order_email_confirmation(order_id)
            time.sleep(5)

        else:
            print("NE NE NE NE NE neposli potvrzeni certifikatu")
            customer_order_email_confirmation(order_id)
            time.sleep(5)

    except ssl.SSLCertVerificationError:
        logging.info(
            f"Local environment, no email sending service. Order ID: {order_id}"
        )
    except smtplib.SMTPSenderRefused as e:
        logging.error(
            f"SMTP Sender Refused Error: {e}. Check SMTP policies. Order ID: {order_id}"
        )

    if settings.DEBUG:
        # Django is running in local settings
        print("Local settings: Zasilkovna turned off")
    elif order.shipping_price == 0:
        print("Local settings: Zasilkovna turned off, shipping price: 0")
    else:
        # Django is running in production settings
        print("Production settings: Zasilkovna turned on")

    if cart.shipping == "Z":
        zasilkovna_create_package(order_id)
        print("Zasilkovna package has been created")
    elif cart.shipping == "P":
        ppl_create_label_view(request, order_id)
        print("PPL package has been created")
    elif cart.shipping == "O":
        print("Online delivery has been requested")

    return render(request, "stripe/completed.html", {"order": order})


def payment_canceled(request):
    try:
        coupon_id = request.session.get("coupon_id")
    except Exception:
        print("there is an exception", Exception)

    order_id = request.session.get("order_id")
    print("oh year this is order_id", order_id)
    cart = Cart(request)

    try:
        customer_order_email_confirmation(order_id)
        print("customer email byl odeslan ale neni zaplaceno")
        time.sleep(5)
    except ssl.SSLCertVerificationError:
        logging.info(
            f"Local environment, no email sending service. Order ID: {order_id}"
        )
    except smtplib.SMTPSenderRefused as e:
        logging.error(
            f"SMTP Sender Refused Error: {e}. Check SMTP policies. Order ID: {order_id}"
        )

    try:
        Coupon.objects.get(id=coupon_id).delete()
    except Coupon.DoesNotExist:
        pass

    if cart.shipping == "Z":
        # zasilkovna_create_package(order_id)
        print("Zasilkovna package has been created")
    elif cart.shipping == "P" or "D":
        ppl_create_label_view(request, order_id)
        print("PPL package has been created")
    elif cart.shipping == "O":
        print("Online delivery has been requested")

    return render(request, "stripe/canceled.html")


import json
import logging

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .api import create_package_label

logger = logging.getLogger(__name__)


@csrf_exempt
def ppl_create_label_view(request, order_id):
    try:
        payload = ppl_create_shipment_payload(
            request, order_id
        )  # Use the helper function to create the payload

        print("this is printing of payload", payload)
        response = create_package_label(payload, request, order_id)

        if not isinstance(response, dict):
            logger.error(f"Unexpected response format: {response}")
            return JsonResponse(
                {"error": "Unexpected response format from the API"}, status=500
            )

        status_code = 201 if response.get("message") else 200

        # Create a response with headers
        response_data = json.dumps(response)
        http_response = HttpResponse(
            response_data, content_type="application/json", status=status_code
        )
        http_response["Custom-Header"] = "CustomHeaderValue"  # Example header

        # Printing the header to the console for debugging purposes
        print(f"Response Headers: {http_response.headers.get}")

        return http_response
    except requests.HTTPError as e:
        logger.error(f"HTTPError: {e.response.text}")
        return JsonResponse({"error": e.response.text}, status=e.response.status_code)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({"error": "An unexpected error occurred"}, status=500)


def ppl_create_shipment_payload(request, order_id):
    # order_id = 289
    order = get_object_or_404(Order, id=order_id)

    print("this is order country", order.country, type(order.country))
    if order.country == "CZ":
        product_type = "BUSS"
    else:
        product_type = "IMPO"
        
        

    print("this is product type", product_type)

    payload = {
        "returnChannel": {"type": "Email", "address": "objednavky@efirthebrand.cz"},
        "labelSettings": {
            "format": "Pdf",
            "dpi": 300,
            "completeLabelSettings": {
                "isCompleteLabelRequested": True,
                "pageSize": "A4",
                "position": 1,
            },
        },
        "shipments": [
            {
                "referenceId": order.etb_id,
                "productType": product_type,
                "shipmentSet": {"numberOfShipments": 1},
                "sender": {
                    "name": "Ing. Valeriya Ageeva",
                    "street": "Příčná 1892/4",
                    "city": " Praha 1 - Nové Město",
                    "zipCode": "11000",
                    "country": "CZ",
                    "contact": "Contact sender",
                    "phone": "+420 774 363 883",
                    "email": "objednavky@efirthebrand.cz",
                },
                "recipient": {
                    "name": f"{order.first_name} {order.last_name}",
                    "street": order.address,
                    "city": order.city,
                    "zipCode": order.zipcode,
                    "country": order.country,
                    "contact": "Kontakt prijemce",
                    "phone": order.number,
                    "email": order.email,
                },
            }
        ],
    }
    return payload


def ppl_track_order():
    pass
