from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from pathlib import Path

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import get_template, render_to_string
from django.urls import reverse
from django.utils.html import strip_tags

from cart.cart import Cart

from .models import Order, OrderItem


def order_email_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    html_content = render_to_string(
        "orders/objednavka_vytvorena.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.id} je potvrzena."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()


from django.core.mail import send_mail


def send_email():
    subject = "Hello"
    message = "This is a test email"
    from_email = "objednavky@efirthebrand.cz"
    recipient_list = ["edgartetour@gmail.com"]

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse("Email sent successfully.")
