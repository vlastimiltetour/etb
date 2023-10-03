from django import forms
from django.shortcuts import get_object_or_404

from catalog.models import Product

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]
"""ZPUSOB_VYROBY_CHOICES = [
    ("Skladem", "Skladem"),
    ("Na_Miru", "Na Míru"),
]"""
"""OBVOD_PRSA_CHOICES = [(obj.id, str(obj)) for obj in ObvodHrudnik.objects.all()]
OBVOD_HRUDNIK_CHOICES = [(obj.id, str(obj)) for obj in ObvodPrsa.objects.all()]

OBVOD_PRSA_CHOICES = [
    (str(i) + j, str(i) + j) for i in range(70, 111, 5) for j in ["A", "B", "C"]
]
OBVOD_PRSA_CHOICES.append((0, "-"))
OBVOD_HRUDNIK_CHOICES = [(i, str(i)) for i in ["XS", "S", "M", "L"]]
OBVOD_HRUDNIK_CHOICES.append((0, "-"))
OBVOD_BOKY_CHOICES = [(i, str(i)) for i in ["XS", "S", "M", "L"]]
OBVOD_BOKY_CHOICES.append((0, "-"))"""


class CartAddProductForm(forms.Form):
    def __init__(self, id_from_product, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        product_id = id_from_product

        product = get_object_or_404(Product, id=product_id)
        available_sizes = []
        velikost = product.get_available_sizes()  # list
        for one_size in velikost:
            available_sizes.append(one_size)
        available_sizes = tuple(sorted(available_sizes))
        available_sizes = [(i, i) for i in available_sizes]

        """obvod_hrudnik = tuple(product.obvod_hrudnik.values_list())
        obvod_hrudnik_list = []
        for item in obvod_hrudnik:
            obvod_hrudnik_list.append(item)
        obvod_hrudnik_list.append((0, "-"))
        obvod_hrudnik_list = sorted(obvod_hrudnik_list)
        """
        """ obvod_hrudnik = tuple(product.obvod_hrudnik.values_list())
        obvod_hrudnik_list = [(i[1], str(i[1])) for i in obvod_hrudnik]
        obvod_hrudnik_list.append(("-", "-"))

        obvod_prsa = tuple(product.obvod_prsa.values_list())
        obvod_prsa_list = [(i[1], str(i[1])) for i in obvod_prsa]
        obvod_prsa_list.append(("-", "-"))

        def extract_numeric_part(value):
            match = re.search(r"\d+", value)
            if match:
                return int(match.group())
            else:
                return float("inf")

        # https://www.regular-expressions.info/refcapture.html
        def extract_letter_part(value):
            match = re.search(r"[A-Za-z]+", value)
            if match:
                return match.group()
            else:
                return ""

        obvod_prsa_list = sorted(
            obvod_prsa_list,
            key=lambda x: (extract_numeric_part(x[1]), extract_letter_part(x[1]))
            if x[1] != "-"
            else (float("inf"), ""),
        )

        obvod_boky = tuple(product.obvod_boky.values_list())
        obvod_boky_list = [(i[1], str(i[1])) for i in obvod_boky]
        obvod_boky_list.append(("-", "-"))

        obvod_body = tuple(product.obvod_body.values_list())
        obvod_body_list = [(i[1], str(i[1])) for i in obvod_body]
        obvod_body_list.append(("-", "-"))

        obvod_body_list = sorted(
            obvod_body_list, key=lambda x: int(x[1]) if x[1] != "-" else float("inf")
        )"""

        zpusob_vyroby = tuple(product.zpusob_vyroby.values_list())
        zpusob_vyroby_list = [(i[1], str(i[1])) for i in zpusob_vyroby]
        # zpusob_vyroby = tuple(product.zpusob_vyroby.values_list())
        # zpusob_vyroby_list = [(i, str(i)) for i in zpusob_vyroby]
        # for item in zpusob_vyroby:
        #    zpusob_vyroby_list.append(item)

        self.fields["quantity"] = forms.TypedChoiceField(
            label="Quantity",
            choices=PRODUCT_QUANTITY_CHOICES,
            coerce=int,
            initial=0,
            widget=forms.Select(attrs={"id": "id_quantity"}),
        )
        self.fields["velikost"] = forms.TypedChoiceField(
            label="Velikost", choices=available_sizes, initial="-"
        )

        self.fields["zpusob_vyroby"] = forms.TypedChoiceField(
            label="Způsob výroby",
            choices=zpusob_vyroby_list,
            initial="Kofekční velikost",
        )
        self.fields["override"] = forms.BooleanField(
            required=False, initial=False, widget=forms.HiddenInput
        )
        self.fields["poznamka"] = forms.CharField(
            label="Poznamka",
            widget=forms.Textarea,
            required=False,
            help_text="Vyplňte tyto hodnoty: Obvod hrudníku Obvod pod hrudníkem Obvod jednoho prsa Obvod pasu Obvod boku",
        )
