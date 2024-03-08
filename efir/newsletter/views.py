import logging
import ssl


from django.http import HttpResponse


from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect, render
from django.template.loader import render_to_string

from .models import Newsletter
from catalog.forms import SubscribeForm
# Create your views here.


def subscribe_test(request):
    return render(request, "newsletter/subs_conf.html")


def subscribe(request):
    subscribe_form = SubscribeForm(request.POST)
    Newsletter.objects.all()
    if request.method == "POST":
        subscribe_form = SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            email = subscribe_form.cleaned_data.get("email")

            if not Newsletter.objects.filter(email=email).exists():
                Newsletter.objects.create(email=email)
                logging.info(f"Email {email} has been saved and sent subscribe confirmation")
                try:
                    customer_order_email_confirmation(email)
                    
                    
                except ssl.SSLCertVerificationError:
                    logging.info("Local environment has no email backend set up. Email: {email}")

                return render(request, 'newsletter/subs_completed.html')


            else:
                logging.info("Email already exists in the database.")
                return HttpResponse("Email already exists in the database.")
        else:
            return HttpResponse("email is not saved")
            
    




def customer_order_email_confirmation(email):
    # html_content = render_to_string("newsletter/subscribe.html")
    html_content = render_to_string("newsletter/subs_conf.html")
    msg = EmailMultiAlternatives(
        subject=("Děkujeme za přihlášení k odběru newsletteru od EFIR"),
        from_email="objednavky@efirthebrand.cz",
        to=[email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()

