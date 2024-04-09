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
    def custom_sort(size):
        if size[:-1].isdigit():
            return int(size[:-1]), size[-1]
        else:
            return float("inf"), size

    def prioritize_sizes(n):
        knickers_dict = {
            "XS": 1,
            "S": 2,
            "M": 3,
            "L": 4,
            "XL": 5,
        }

        knickers = []
        bras = []
        for size in n:
            if size in knickers_dict:
                knickers.append(size)
            else:
                bras.append(size)

        knickers.sort(key=lambda x: knickers_dict[x])

        print(knickers)
        return knickers + bras

    all_sizes = Inventory.objects.all()
    all_sizes = all_sizes.distinct()
    all_sizes = all_sizes.values_list("size")
    letters_only = [size[0].strip("()") for size in all_sizes if size[0]]
    sorted_sizes = sorted(letters_only, key=custom_sort)
    resorted_sizes = prioritize_sizes(sorted_sizes)
    tuple_sizes = [(size, size) for size in resorted_sizes]
    print("size_choices:", resorted_sizes)

    products = Product.objects.all()

    cuts_all = products.values_list("short_description").distinct()
    cuts_letters_only = [x[0].strip("()") for x in cuts_all if x[0]]
    cuts_all_list = set(cuts_letters_only)
    cut_choices = [(i, i) for i in cuts_all_list]

    cut_choices_manual = [
        ("Brazilky", "Brazilky"),
        ("Brazilky na gumičkách", "Brazilky na gumičkách"),
        ("V-string", "V-string"),
        ("Vysoká tanga", "Vysoká tanga"),
        ("Podvazkový pás s gumičkami", "Podvazkový pás s gumičkami"),
        ("Bezkosticová podprsenka", "Bezkosticová podprsenka"),
        ("Podprsenka s kosticemi", "Podprsenka s kosticemi"),
        (
            "Podprsenka s kosticemi a otevřeným košíčkem",
            "Podprsenka s kosticemi a otevřeným košíčkem",
        ),
    ]

    categories = Category.objects.all()
    categories = categories.values_list("name").distinct()
    categories = [name[0].strip("()") for name in categories]
    categories = [(i, i) for i in categories]

    size_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=tuple_sizes,
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
        choices=cut_choices_manual,
        label="Volba střihu",
        required=False,
    )

    category_selection = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=categories,
        label="Volba kategorie",
        required=False,
    )


class CreateSetForm(forms.Form):
    # captcha = ReCaptchaField()

    name = forms.CharField(
        label="Vaše jméno",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    surname = forms.CharField(
        label="Vaše příjmení",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        max_length=50,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email, který bežně používáte...",
            }
        ),
    )
    # opravit
    birthday = forms.DateField(
        label="Kdy jste se narodila?",
        widget=forms.DateInput(attrs={"class": "form-control"}),
    )

    hair_color = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 9)],
        label="Jakou máte barvu vlasů:",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    skin_color = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 7)],
        label="Který odstín kůže na obrázku je nejvíce podobný té vaší:",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    color_tone = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Neutrální barvy (černá, bílá, béžová)",
                "Pastelové tóny (růžová, světlé modrá, levandule)",
                "Tmavší tóny (tmavě modrá, smaragdová, bordo)",
                "Výrazné barvy (červená, lavandule, tyrkysová)",
            ]
        ],
        label="Jaký je váš oblíbený barevný odstín, ve kterém se cítíte nejlépe?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    colors_to_avoid = forms.ChoiceField(
        choices=[(i, i) for i in ["Neexistují", "Jiné"]],
        label="Existují barvy, kterým se snažíte vyhýbat?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    other_colors = forms.CharField(
        label="Jiné barvy, kterým se snažíte vyhýbat:",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "kterou nikdy nevyberete na spodní prádlo...",
            }
        ),
    )

    def set_other_colors(self):
        colors_to_avoid = self.cleaned_data.get("colors_to_avoid", None)

        if colors_to_avoid != "Jiné":
            self.cleaned_data["other_colors"] = "-"

    design_preferences = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Jednoduchý a elegantní",
                "S decentními vzory",
                "S výraznými vzory a detaily",
            ]
        ],
        label="Máte raději jednoduchý a elegantní design, nebo preferujete spodní prádlo s výraznými vzory a detaily?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    overall_fitness = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Ano, je to pro mě důležité",
                "Někdy, záleží na příležitosti",
                "Ne, spodní prádlo je pro mě samostatným prvkem",
            ]
        ],
        label="Když si vybíráte spodní prádlo, berete v potaz, jak ladí s vaším běžným oblečením?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    individual_cut = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Pohodlí má pro mě prioritu",
                "Obojí, ideálně kombinace pohodlí a stylu",
                "Styl je pro mě klíčový",
            ]
        ],
        label="Je pro vás důležitý pohodlný střih, nebo upřednostňujete spodní prádlo, které zdůrazňuje váš individuální styl?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    knickers_cut = forms.ChoiceField(
        choices=[(i, i) for i in ["Brazilky", "Tanga", "Slipy"]],
        label="Který střih kalhotek je pro Vás nejpohodlnější?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    bra_cut = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Podprsenka s kosticemi",
                "Podprsenka bez kostic",
                "Podprsenka s výrazným střihem",
            ]
        ],
        label="Který střih podprsenky poskytuje komfortní nošení?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    activities = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Každodenní nošení",
                "Při sportovních aktivitách",
                "Speciální příležitosti",
            ]
        ],
        label="V jakých příležitostech nosíte spodní prádlo nejčastěji?",
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    preferred_details = forms.CharField(
        required=False,
        label="Existují nějaké specifické vlastnosti nebo detaily, na které jste zvyklá a které byste chtěla u vysněného setu? (volná odpověď)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Oceníme každé slovo..."}
        ),
    )

    gdpr_consent = forms.BooleanField(
        label="Souhlas se zpracováním osobních údajů.",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    newsletter_consent = forms.BooleanField(
        label="Souhlas s odebíráním newsletteru.",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    """
Pak tlačítko odeslat. + tlačítko souhlas se zpracováním osobních údajů, tlačítko s odebráním newslatter (oba jsou povinné zaškrtnout)
(Logo a poděkování) Děkujeme za vyplnění dotazníku! Vaše odpověď bude pečlivě zpracována a dostanete ve výsledku zašleme Vám na email nabídku setu o kterých jste snili . Do 2 pracovních dnů dostanete na email svůj vysněný set. 
"""


"""Pod jméno, příjmení, e-mail atd, musí být polyčko pro “Popište o který set byste měla zájem?” A pak odeslat"""


class MappingSetNaMiruForm(forms.Form):
    captcha = ReCaptchaField()

    name = forms.CharField(
        label="Vaše jméno",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    surname = forms.CharField(
        label="Vaše příjmení",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        max_length=50,
        validators=[EmailValidator()],
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Email, který bežně používáte...",
            }
        ),
    )
    number = forms.CharField(
        label="Vaše telefonní číslo",
        max_length=50,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    set_selection = forms.CharField(
        label="Tady se můžete zeptat na cokoli",
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "sem vepište set, který jste vybrala, požadavky, nebo otázky...",
            }
        ),
    )
    gdpr_consent = forms.BooleanField(
        label="Souhlas se zpracováním osobních údajů",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )
    newsletter_consent = forms.BooleanField(
        label="Souhlas s odebíráním newsletteru",
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    """
Pak tlačítko odeslat. + tlačítko souhlas se zpracováním osobních údajů, tlačítko s odebráním newslatter (oba jsou povinné zaškrtnout)
(Logo a poděkování) Děkujeme za vyplnění dotazníku! Vaše odpověď bude pečlivě zpracována a dostanete ve výsledku zašleme Vám na email nabídku setu o kterých jste snili . Do 2 pracovních dnů dostanete na email svůj vysněný set. 
"""


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
