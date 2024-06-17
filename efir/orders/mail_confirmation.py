from io import BytesIO
from smtplib import (SMTPDataError, SMTPException, SMTPRecipientsRefused,
                     SMTPSenderRefused)

import weasyprint
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Order


def customer_order_email_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    pdf = render_to_string("orders/invoice_pdf.html", {"order": order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / "css/styles.css")]
    weasyprint.HTML(string=pdf).write_pdf(out, stylesheets=stylesheets)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    ) 
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["v.tetour@gmail.com", "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f"Objednavka {order.etb_id}.pdf", out.getvalue(), "application/pdf")

    return msg.send()


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Order


def customer_order_email_confirmation_X(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["objednavky@efirthebrand.cz"]
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def certificate_order_email_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/certificate_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=("Váš zakoupený certifikát od EFIR"),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def send_offer_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=f"Vaše objednávka #{order.etb_id} je potvrzena.",
        from_email="objednavky@efirthebrand.cz",
        to=[order.email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
        return HttpResponse("Confirmation email sent successfully.")
    except SMTPSenderRefused as e:
        print(f"Sender address refused: {e}")
    except SMTPRecipientsRefused as e:
        print(f"Recipient address refused: {e}")
    except SMTPDataError as e:
        print(f"SMTP data error: {e}")
    except SMTPException as e:
        # Generic handler for any other SMTP-related errors
        print(f"Failed to send email: {e}")
        # Handle the exception (e.g., log the error, retry sending, etc.)

    return HttpResponse("Email wasn't sent")
