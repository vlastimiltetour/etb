import logging
import ssl

from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.template.loader import render_to_string

from .models import Newsletter

# Create your views here.


def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not Newsletter.objects.filter(email=email).exists():
            Newsletter.objects.create(email=email)
            logging.info(
                f"Email {email} has been saved and sent subscribe confirmation"
            )
            try:
                customer_order_email_confirmation(email)
            except ssl.SSLCertVerificationError:
                logging.info(
                    f"Local environment has no email backend set up.Email: {email}"
                )

        else:
            logging.info(
                "there is an error with object creation, email either exist or is an empty value."
            )

    return redirect("catalog:home")


def customer_order_email_confirmation(email):
    # html_content = render_to_string("newsletter/subscribe.html")
    html_content = render_to_string("orders/customer_email_confirmation.html")
    msg = EmailMultiAlternatives(
        subject=("Děkujeme za odběr."),
        from_email="objednavky@efirthebrand.cz",
        to=[email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
