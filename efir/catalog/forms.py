from django import forms
from django.core.validators import EmailValidator
from django_recaptcha.fields import ReCaptchaField

from catalog.models import Category, Product
from inventory.models import Inventory


class ContactForm(forms.Form):
    captcha = ReCaptchaField()

    name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Vaše jméno"}
        ),
    )
    email = forms.EmailField(
        max_length=50,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Email"}
        ),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": "Text"}),
        required=True,
    )


class FilterForm(forms.Form):
    all_sizes = Inventory.objects.all()
    all_sizes = all_sizes.distinct()
    all_sizes = all_sizes.values_list("size")
    letters_only = [size[0].strip("()") for size in all_sizes if size[0]]
    all_sizes = [(size, size) for size in letters_only]
    size_choices = all_sizes

    products = Product.objects.all()

    cuts_all = products.values_list("short_description").distinct()
    cuts_letters_only = [x[0].strip("()") for x in cuts_all if x[0]]
    cuts_all_list = set(cuts_letters_only)
    cut_choices = [(i, i) for i in cuts_all_list]

    categories = Category.objects.all()
    categories = categories.values_list("name").distinct()
    categories = [name[0].strip("()") for name in categories]
    categories = [(i, i) for i in categories]

  

    size_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=size_choices,
        label="Velikost",
        required=False,
    )

    sorting_choices = [
        ("price", "Cena vzestupně"),
        ("-price", "Cena sestupně"),
        ("name", "Název A-Z"),
        ("-name", "Název Z-A"),
    ]

    sort_by_price = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=sorting_choices,
        label="Radit podle",
        required=False,
    )

    zpusob_vyroby_choices = [
        ("Skladem", "Skladem"),
        ("Na Míru", "Na Míru"),
    ]

    zpusob_vyroby = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=zpusob_vyroby_choices,
        label="Zpusob vyroby",
        required=False,
    )

    cut_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=cut_choices,
        label="Volba střihu",
        required=False,
    )

    category_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=categories,
        label="Volba kategorie",
        required=False,
    )
