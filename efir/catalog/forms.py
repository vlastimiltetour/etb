from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
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
