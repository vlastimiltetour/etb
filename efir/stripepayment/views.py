import base64
import io
import json
import logging
from decimal import Decimal

import requests
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from reportlab.lib.pagesizes import A4, A6, A7, A8
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from coupons.views import coupon_delete
from efir.settings.base import ZASILKOVNA_SECRET
from orders.models import Order

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION

import xml.etree.ElementTree as ET


def payment_process(request):
    order_id = request.session.get("order_id")
    # order_id = 4

    order = get_object_or_404(Order, id=order_id)

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
            return render(request, "stripe/canceled.html")

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

    # Create a dictionary representing the order details
    order_details = {
        "apiPassword": api_password,
        "packetAttributes": {
            "number": order_id,
            "name": order_name,
            "surname": order_surname,
            "email": order_email,
            "addressId": vendor_id,
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

            packetLabelPdf(packetId=packet_id, format="A7 on A4", offset=0)
        except AttributeError as e:
            print("An error occurred while parsing the XML response:", e)


# TODO finish this packet label pdf download
def packetLabelPdf(packetId, format="A7 on A4", offset=0):
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
    response_contents = response.text
    decoded_data = base64.b64decode(response_contents)

    # write the decoded data back to original format in  file
    img_file = open("image.jpeg", "wb")
    img_file.write(decoded_data)
    img_file.close()

    return decoded_data


# ----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----


def packetLabelPdf2(packetId, format="A7 on A4", offset=0):
    # Validate the format parameter
    allowed_formats = {
        "A6 on A6": (A6, A6),
        "A7 on A7": (A7, A7),
        "A6 on A4": (A6, A4),
        "A7 on A4": (A7, A4),
        "105x35mm on A4": ((105 * mm, 35 * mm), A4),
        "A8 on A8": (A8, A8),
    }

    if format not in allowed_formats:
        raise UnknownLabelFormatFault("Unknown label format")

    packet_data = f"Packet ID: {packetId}\nOther details: ..."  # Replace with actual packet details

    # Create the PDF using ReportLab
    packet_width, packet_height = allowed_formats[format][0]
    page_width, page_height = allowed_formats[format][1]

    buffer = io.BytesIO()
    c = canvas.Canvas(
        buffer,
        pagesize=(page_width, page_height)
        if offset == 0
        else (page_height, page_width),
    )
    if offset > 0:
        c.translate(offset * mm, 0)

    # Draw the label
    c.setFont("Helvetica", 12)
    c.drawString(10 * mm, page_height - 20 * mm, packet_data)

    corner_radius = 5  # Adjust the corner radius as needed
    c.roundRect(
        5 * mm, page_height - 25 * mm, packet_width, packet_height, corner_radius
    )

    c.save()

    # Save the PDF to a file
    pdf_filename = f"label_{packetId}.pdf"
    with open(pdf_filename, "wb") as pdf_file:
        pdf_file.write(buffer.getvalue())

    # Set the content type and filename for the response
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{pdf_filename}"'
    response.write(buffer.getvalue())

    buffer.close()

    return response


# ----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----#----


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
    #todo finish coupon delete
    '''if coupon: 
        coupon_delete(request)'''

    order = get_object_or_404(Order, id=order_id)
    return render(request, "stripe/completed.html", {"order": order})


def payment_canceled(request):
    return render(request, "stripe/canceled.html")


def notify(request):
    pass


## this should be placed in a separate app


"""
def create_package():
    pass



def export_to_zasilkovna():
    api_key = ZASILKOVNA_SECRET
    endpoint = "https://api.zasilkovna.cz/v4/orders"

    headers = {
        "Authorization": f"ApiKey {api_key}",
        "Content-Type": "application/json"
    }

    order_details = 
    response = requests.post(endpoint, json=order_details, headers=headers)

    if response.status_code == 201:
        return True
    else:
        return False
"""
