from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "number",
            "comments",
            "shipping",
            "address",
            "country",
            "vendor_id",
        ]

        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Napište své jméno"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Napište své příjmení"}
            ),
            "email": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Napište svůj e-mail"}
            ),
            "number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Napište své číslo"}
            ),
            "comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Zde můžete vložit své komentáře k objednávce.",
                    "initial": "-",
                }
            ),
            "shipping": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vyberte si způsob dopravy",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte adresu, kam doručit oblečení",
                }
            ),
            "vendor_id": forms.HiddenInput(),
            "country": forms.Select(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte adresu, kam doručit oblečení",
                },
            ),
        }
