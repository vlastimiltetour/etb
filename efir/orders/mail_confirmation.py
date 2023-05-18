from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Order


def customer_order_email_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.id} je potvrzena."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
