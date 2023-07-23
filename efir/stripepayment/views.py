import json
import logging
from decimal import Decimal

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse

from orders.models import Order

# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        success_url = request.build_absolute_uri(reverse("stripepayment:completed"))
        cancel_url = request.build_absolute_uri(reverse("stripepayment:canceled"))

        # Stripe checkout session data
        session_data = {
            "mode": "payment",
            "client_reference_id": order.id,
            "success_url": success_url,
            "cancel_url": cancel_url,
            "line_items": [],
        }
        # Add order items to the Stripe checkout session
        for item in order.items.all():
            session_data["line_items"].append(
                {
                    "price_data": {
                        "unit_amount": int(item.price * Decimal("100")),
                        "currency": "czk",
                        "product_data": {
                            "name": item.product.name,
                        },
                    },
                    "quantity": item.quantity,
                }
            )

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(**session_data)

        # Redirect to Stripe payment form
        return redirect(checkout_session.url)

    else:
        return render(request, "stripe/process.html", locals())


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
    return render(request, "stripe/completed.html")


def payment_canceled(request):
    return render(request, "stripe/canceled.html")


def notify(request):
    pass
