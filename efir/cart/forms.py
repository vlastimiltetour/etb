from django import forms

from catalog.models import Product

# this snippet of code is to change integers to string for serialization purpose
PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
KONFEKCNI_OBVOD_PRSA = [
    (obj.id, str(obj)) for obj in Product.objects.get(id).obvod_hrudnik.all()
]
KONFEKCNI_OBVOD_HRUDNIK = [
    (obj.id, str(obj)) for obj in Product.objects.get(id).obvod_prsa.all()
]


ZPUSOB_VYROBY_CHOICES = [
    ("Na_Miru", "Na Míru"),
    ("Konfekce", "Konfekce"),
]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label="quantity", choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )

    obvod_prsa = forms.TypedChoiceField(
        label="obvod_prsa",
        choices=KONFEKCNI_OBVOD_PRSA,
        coerce=int,
    )
    obvod_hrudnik = forms.TypedChoiceField(
        label="obvod_hrudnik",
        choices=KONFEKCNI_OBVOD_HRUDNIK,
        coerce=int,
    )

    zpusob_vyroby = forms.ChoiceField(
        label="zpusob_vyroby", choices=ZPUSOB_VYROBY_CHOICES
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
