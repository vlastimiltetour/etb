from django import forms

KONFEKCNI_OBVOD_PRSA = [(i, str(i)) for i in range(18, 26)]
KONFEKCNI_OBVOD_HRUDNIK = [(i, str(i)) for i in range(79, 110)]


class KonfekcniVelikostObdovPrsa(forms.Form):
    obvod_prsa = forms.TypedChoiceField(
        label="count", choices=KONFEKCNI_OBVOD_PRSA, coerce=int
    )


class KonfekcniVelikostObdovHrudnik(forms.Form):
    obvod_hrudnik = forms.TypedChoiceField(
        label="count", choices=KONFEKCNI_OBVOD_HRUDNIK, coerce=int
    )


class NaMiruVelikostObdovPrsa(forms.Form):
    size = forms.TypedChoiceField(
        label="count", choices=KONFEKCNI_OBVOD_PRSA, coerce=int
    )


class NaMiruVelikostObdovHrudnik(forms.Form):
    size = forms.TypedChoiceField(
        label="count", choices=KONFEKCNI_OBVOD_HRUDNIK, coerce=int
    )
