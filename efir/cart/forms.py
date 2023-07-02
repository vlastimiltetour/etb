from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
ZPUSOB_VYROBY_CHOICES = [
    ("Konfekce", "Konfekce"),
    ("Na_Miru", "Na Míru"),
]
# OBVOD_PRSA_CHOICES = [(obj.id, str(obj)) for obj in ObvodHrudnik.objects.all()]
# OBVOD_HRUDNIK_CHOICES = [(obj.id, str(obj)) for obj in ObvodPrsa.objects.all()]
OBVOD_PRSA_CHOICES = [(i, str(i)) for i in range(79, 111)]
OBVOD_PRSA_CHOICES.append((0, "-"))
OBVOD_HRUDNIK_CHOICES = [(i, str(i)) for i in range(19, 26)]
OBVOD_HRUDNIK_CHOICES.append((0, "-"))
OBVOD_BOKY_CHOICES = [(i, str(i)) for i in range(22, 44)]
OBVOD_BOKY_CHOICES.append((0, "-"))


"""Cely set
Velikosti podprsenky (70A-85C) 
Velikost pasu (XS-L) 
Velikost kalhotek (XS-L)"""


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
        label="Quantity", choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=0
    )
    obvod_prsa = forms.TypedChoiceField(
        label="Obvod prsa", choices=OBVOD_PRSA_CHOICES, coerce=int, initial=0
    )
    obvod_boky = forms.TypedChoiceField(
        label="Obvod boky", choices=OBVOD_BOKY_CHOICES, coerce=int, initial=0
    )
    obvod_hrudnik = forms.TypedChoiceField(
        label="Obvod hrudník", choices=OBVOD_HRUDNIK_CHOICES, coerce=int, initial=0
    )
    zpusob_vyroby = forms.ChoiceField(
        label="Způsob výroby",
        choices=ZPUSOB_VYROBY_CHOICES,
        initial="Kofekční velikost",
    )
    override = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )
    poznamka = forms.CharField(
        label="Poznamka",
        widget=forms.Textarea,
        required=False,
        help_text="Vyplňte tyto hodnoty: Obvod hrudníku Obvod pod hrudníkem Obvod jednoho prsa Obvod pasu Obvod boku",
    )
