
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from catalog.models import MappingSetNaMiru


def siti_na_miru_email_confirmation(mapping_id):
    mapping_siti_na_miru = MappingSetNaMiru.objects.get(id=mapping_id)
    html_content = render_to_string("catalog/siti_na_miru_confirmation.html")
    msg = EmailMultiAlternatives(
        subject=("Potvrzení přijetí požadavku na prádlo na míru EFIR the brand"),
        from_email="objednavky@efirthebrand.cz",
        to=[mapping_siti_na_miru.email, "objednavky@efirthebrand.cz"],
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
