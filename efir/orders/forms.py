from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    agree_to_terms = forms.BooleanField(
        required=True,  # You can set this to False if it's optional
        label="I agree to the terms and conditions",  # Change the label as needed
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "number",
            "birthday",
            "comments",
            "shipping",
            "address",
            "country",
            "vendor_id",
            "newsletter_consent",
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
            "birthday": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Napište své datum narození",
                },
            ),
            "comments": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Zde můžete vložit své komentáře k objednávce.",
                    "initial": "-",
                }
            ),
            "shipping": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vyberte si způsob dopravy",
                }
            ),
            "address": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte adresu, kam doručit oblečení",
                    # "readonly": True,  # Add the readonly attribute here
                }
            ),
            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte mesto, kam doručit oblečení",
                    # "readonly": True,  # Add the readonly attribute here
                }
            ),
            "zipcode": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte zipcode, kam doručit oblečení",
                    # "readonly": True,  # Add the readonly attribute here
                }
            ),
            "vendor_id": forms.HiddenInput(),
            "shipping_price": forms.HiddenInput(),
            "country": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Vložte adresu, kam doručit oblečení",
                    # "readonly": True,
                },
            ),
            "newsletter_consent": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }
