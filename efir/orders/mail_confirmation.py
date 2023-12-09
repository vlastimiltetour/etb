from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from io import BytesIO
import weasyprint
from .models import Order
from django.conf import settings


def customer_order_email_confirmation(order_id):
    
    order = Order.objects.get(id=order_id)
    pdf = render_to_string('orders/invoice_pdf.html', {"order": order})
    out = BytesIO()
    stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / "css/styles.css")]
    weasyprint.HTML(string=pdf).write_pdf(out, stylesheets=stylesheets)
    html_content = render_to_string(
        "orders/customer_email_confirmation.html", {"order": order}
    )
    msg = EmailMultiAlternatives(
        subject=(f"Vaše objednávka #{order.etb_id} je potvrzena."),
        from_email="objednavky@efirthebrand.cz",
        to=[order.email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.attach(f'Objednavka {order.etb_id}.pdf',out.getvalue(),'application/pdf')
    
    return msg.send()
