from django import forms

from catalog.models import ObvodHrudnik, ObvodPrsa

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
ZPUSOB_VYROBY_CHOICES = [
    ("Na_Miru", "Na Míru"),
    ("Konfekce", "Konfekce"),
]
OBVOD_PRSA_CHOICES = [(obj.id, str(obj)) for obj in ObvodHrudnik.objects.all()]
OBVOD_HRUDNIK_CHOICES = [(obj.id, str(obj)) for obj in ObvodPrsa.objects.all()]
#OBVOD_PRSA_CHOICES = [(i, str(i)) for i in range(1, 21)]
#OBVOD_HRUDNIK_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label="Quantity", choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )
    obvod_prsa = forms.TypedChoiceField(
        label="Obvod prsa", choices=OBVOD_PRSA_CHOICES, coerce=int
    )
    obvod_hrudnik = forms.TypedChoiceField(
        label="Obvod hrudník", choices=OBVOD_HRUDNIK_CHOICES, coerce=int
    )
    zpusob_vyroby = forms.ChoiceField(
        label="Způsob výroby", choices=ZPUSOB_VYROBY_CHOICES
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
