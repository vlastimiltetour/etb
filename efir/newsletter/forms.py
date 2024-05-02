from django import forms
from django.core.validators import EmailValidator
from django_recaptcha.fields import ReCaptchaField


class SubscribeForm(forms.Form):
    captcha = ReCaptchaField()

    email = forms.EmailField(
        max_length=50,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Vložte Váš email, který bežně používáte...",
            }
        ),
    )



class UnsubscribeForm(forms.Form):
    # captcha = ReCaptchaField()

    email = forms.EmailField(
        max_length=50,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Vložte Váš email, který chcete smazat...",
            }
        ),
    )

