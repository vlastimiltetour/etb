from django import forms
from django.shortcuts import get_object_or_404, render

from catalog.models import Product

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
ZPUSOB_VYROBY_CHOICES = [
    ("Konfekce", "Konfekce"),
    ("Na_Miru", "Na Míru"),
]
# OBVOD_PRSA_CHOICES = [(obj.id, str(obj)) for obj in ObvodHrudnik.objects.all()]
# OBVOD_HRUDNIK_CHOICES = [(obj.id, str(obj)) for obj in ObvodPrsa.objects.all()]
OBVOD_PRSA_CHOICES = [
    (str(i) + j, str(i) + j) for i in range(70, 111, 5) for j in ["A", "B", "C"]
]
OBVOD_PRSA_CHOICES.append((0, "-"))
OBVOD_HRUDNIK_CHOICES = [(i, str(i)) for i in ["XS", "S", "M", "L"]]
OBVOD_HRUDNIK_CHOICES.append((0, "-"))
OBVOD_BOKY_CHOICES = [(i, str(i)) for i in ["XS", "S", "M", "L"]]
OBVOD_BOKY_CHOICES.append((0, "-"))


class CartAddProductForm(forms.Form):
    def __init__(self, id_from_product, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        product_id = id_from_product
        
        product = get_object_or_404(Product, id=product_id)
   
        obvod_hrudnik = tuple(product.obvod_hrudnik.values_list())  
        obvod_hrudnik_list = []
        for item in obvod_hrudnik:
            obvod_hrudnik_list.append(item)

        obvod_prsa = tuple(product.obvod_prsa.values_list())  
        obvod_prsa_list = []
        for item in obvod_prsa:
            obvod_prsa_list.append(item)

        obvod_boky = tuple(product.obvod_boky.values_list())  
        obvod_boky_list = []
        for item in obvod_boky:
            obvod_boky_list.append(item)

        self.fields['quantity'] = forms.TypedChoiceField(
            label="Quantity", choices=PRODUCT_QUANTITY_CHOICES, coerce=int, initial=0
        )
        self.fields['obvod_prsa'] = forms.TypedChoiceField(
            label="Obvod prsa", choices=obvod_prsa_list, coerce=int, initial=0
        )
        self.fields['obvod_boky'] = forms.TypedChoiceField(
            label="Obvod boky", choices=obvod_boky_list, coerce=int, initial=0
        )
        self.fields['obvod_hrudnik'] = forms.TypedChoiceField(
            label="Obvod hrudník", choices=obvod_hrudnik_list, coerce=int, initial=0
        )
        self.fields['zpusob_vyroby'] = forms.ChoiceField(
            label="Způsob výroby",
            choices=ZPUSOB_VYROBY_CHOICES,
            initial="Kofekční velikost",
        )
        self.fields['override'] = forms.BooleanField(
            required=False, initial=False, widget=forms.HiddenInput
        )
        self.fields['poznamka'] = forms.CharField(
            label="Poznamka",
            widget=forms.Textarea,
            required=False,
            help_text="Vyplňte tyto hodnoty: Obvod hrudníku Obvod pod hrudníkem Obvod jednoho prsa Obvod pasu Obvod boku",
        )
