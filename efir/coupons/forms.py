from django import forms

from .models import Coupon


class CouponForm(forms.Form):
    model = Coupon
    code = forms.CharField(
        label="",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Slevový kód"}
        ),
    )
