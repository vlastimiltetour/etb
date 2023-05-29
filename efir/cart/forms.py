from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
KONFEKCNI_OBVOD_PRSA = [(i, str(i)) for i in range(18, 26)]
KONFEKCNI_OBVOD_HRUDNIK = [(i, str(i)) for i in range(79, 110)]

ZPUSOB_VYROBY_CHOICES = [
    ("na_miru", "Na Míru"),
    ("konfekcni_velikost", "Konfekční velikost"),
]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label="quantity", choices=PRODUCT_QUANTITY_CHOICES, coerce=int
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
    obvod_prsa = forms.TypedChoiceField(
        label="obvod_prsa", choices=KONFEKCNI_OBVOD_PRSA, coerce=int
    )
    obvod_hrudnik = forms.TypedChoiceField(
        label="obvod_hrudnik", choices=KONFEKCNI_OBVOD_HRUDNIK, coerce=int
    )
    zpusob_vyroby = forms.ChoiceField(
        label="zpusob_vyroby", choices=ZPUSOB_VYROBY_CHOICES
    )
