import logging
import urllib.error
from io import BytesIO
from smtplib import (SMTPDataError, SMTPException, SMTPRecipientsRefused,
                     SMTPSenderRefused)

import weasyprint
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Order

"""# Set up Django environment
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "efir.settings.base"
)  # Replace 'myproject' with the name of your Django project
django.setup()"""

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def customer_order_email_confirmation(order_id):
    try:
        logger.info(
            "Attempting to send customer order confirmation email for order ID %s",
            order_id,
        )

        order = Order.objects.get(id=order_id)
        pdf = render_to_string("orders/invoice_pdf.html", {"order": order})
        out = BytesIO()
        stylesheet_url = (
            "https://etb.fra1.cdn.digitaloceanspaces.com/etb/css/styles.css"
        )
        # stylesheet_url = f"{settings.STATIC_URL}css/styles.css"
        print("this is stylesheet url", stylesheet_url)

        try:
            stylesheets = [weasyprint.CSS(stylesheet_url)]
            weasyprint.HTML(string=pdf).write_pdf(out, stylesheets=stylesheets)
        except urllib.error.URLError as e:
            logger.error("Failed to fetch stylesheet: %s", e)
            stylesheets = []  # Proceed without stylesheets if fetching fails

        html_content = render_to_string(
            "orders/customer_email_confirmation.html", {"order": order}
        )
        msg = EmailMultiAlternatives(
            subject=f"Vaše objednávka #{order.etb_id} je potvrzena [ZAPLACENO].",
            from_email="objednavky@efirthebrand.cz",
            to=[order.email],
            bcc=["objednavky@efirthebrand.cz"],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.attach(f"Objednavka {order.etb_id}.pdf", out.getvalue(), "application/pdf")

        msg.send()
        logger.info(
            "Customer order confirmation email sent successfully for order ID %s",
            order_id,
        )
        return True

    except (
        SMTPDataError,
        SMTPException,
        SMTPRecipientsRefused,
        SMTPSenderRefused,
    ) as e:
        logger.error("Failed to send email: %s", e)
        return False

    except Order.DoesNotExist:
        logger.error("Order with ID %s does not exist", order_id)
        return False

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        logger.info(
            "Attempting to send customer order confirmation email for order ID without PDF %s",
            order_id,
        )

        order = Order.objects.get(id=order_id)

        html_content = render_to_string(
            "orders/customer_email_confirmation.html", {"order": order}
        )
        msg = EmailMultiAlternatives(
            subject=f"Vaše objednávka #{order.etb_id} je potvrzena [ZAPLACENO].",
            from_email="objednavky@efirthebrand.cz",
            to=[order.email],
            bcc=["objednavky@efirthebrand.cz"],
        )
        msg.attach_alternative(html_content, "text/html")

        msg.send()
        logger.info(
            "Customer order confirmation email sent successfully wihtout PDF for order ID %s",
            order_id,
        )

        return False


from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Order


def unpaid_customer_order_email_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/unpaid_customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena [NEUHRAZENO]"),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def certificate_order_email_confirmation(order_id):
    try:
        order = Order.objects.get(id=order_id)
        pdf = render_to_string("orders/invoice_pdf.html", {"order": order})
        out = BytesIO()
        stylesheet_url = (
            "https://etb.fra1.cdn.digitaloceanspaces.com/etb/css/styles.css"
        )
        stylesheets = [weasyprint.CSS(stylesheet_url)]
        weasyprint.HTML(string=pdf).write_pdf(out, stylesheets=stylesheets)

        html_content = render_to_string(
            "orders/certificate_confirmation.html", {"order": order}
        )
        msg = EmailMultiAlternatives(
            subject=("Váš zakoupený certifikát od EFIR"),
            from_email="objednavky@efirthebrand.cz",
            to=[order.email],
            bcc=["objednavky@efirthebrand.cz"],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.attach(f"Objednavka {order.etb_id}.pdf", out.getvalue(), "application/pdf")

        return msg.send()

    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        logger.info(
            "Attempting to send certificate order confirmation email for order ID without PDF %s",
            order_id,
        )
        order = Order.objects.get(id=order_id)
        html_content = render_to_string(
            "orders/certificate_confirmation.html", {"order": order}
        )
        msg = EmailMultiAlternatives(
            subject=("Váš zakoupený certifikát od EFIR"),
            from_email="objednavky@efirthebrand.cz",
            to=[order.email],
            bcc=["objednavky@efirthebrand.cz"],
        )
        msg.attach_alternative(html_content, "text/html")
        return msg.send()


def send_offer_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/unpaid_customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena [NEUHRAZENO]"),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["objednavky@efirthebrand.cz"],
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


def send_paid_offer_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena [ZAPLACENO]."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


def order_shipped(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string("orders/order_shipped.html", {"order": order})
    msg = EmailMultiAlternatives(
        subject=(
            f"Předali jsme objednávku dopravci." 
        ),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
        bcc=["objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
