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
    name = forms.CharField(
        label="1. Vaše jméno",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Vaše jméno"}
        ),
    )

    surname = forms.CharField(
        label="2. Vaše příjmení",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Vaše příjmení"}
        ),
    )

    # opravit
    birthday = forms.DateField(
        label="3. Kdy jste se narodila?",
        widget=forms.DateInput(
            attrs={"class": "form-control", "placeholder": "DD MM RRRR"}
        ),
    )

    hair_color = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 9)],
        label="4. Jakou máte barvu vlasů:",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    skin_color = forms.ChoiceField(
        choices=[(i, i) for i in range(1, 7)],
        label="5. Který odstín kůže na obrázku je nejvíce podobný té vaší:",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
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
        label="1. Jaký je váš oblíbený barevný odstín, ve kterém se cítíte nejlépe?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    colors_to_avoid = forms.ChoiceField(
        choices=[(i, i) for i in ["Neexistují", "Jiné"]],
        label="2. Existují barvy, kterým se snažíte vyhýbat?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    design_preferences = forms.ChoiceField(
        choices=[
            (i, i)
            for i in [
                "Jednoduchý a elegantní",
                "S decentními vzory",
                "S výraznými vzory a detaily",
            ]
        ],
        label="3. Máte raději jednoduchý a elegantní design, nebo preferujete spodní prádlo s výraznými vzory a detaily?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
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
        label="4. Když si vybíráte spodní prádlo, berete v potaz, jak ladí s vaším běžným oblečením?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
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
        label="5. Je pro vás důležitý pohodlný střih, nebo upřednostňujete spodní prádlo, které zdůrazňuje váš individuální styl?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    knickers_cut = forms.ChoiceField(
        choices=[(i, i) for i in ["Brazilky", "Tanga", "Slipy"]],
        label="6. Který střih kalhotek dělá pro Vás největší pohodli?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
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
        label="7. Který střih podprsenky poskytuje komfortní nošení?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
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
        label="8. V jakých příležitostech nosíte spodní prádlo nejčastěji?",
        widget=forms.Select(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    preferred_details = forms.CharField(
        required=False,
        label="9. Existují nějaké specifické vlastnosti nebo detaily, na které jste zvyklá a které byste chtěla u vysněného setu? (volná odpověď)",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Vaše odpověď"}
        ),
    )

    gdpr_consent = forms.BooleanField(
        label="Souhlas se zpracováním osobních údajů",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    captcha = ReCaptchaField()

    """
Pak tlačítko odeslat. + tlačítko souhlas se zpracováním osobních údajů, tlačítko s odebráním newslatter (oba jsou povinné zaškrtnout)
(Logo a poděkování) Děkujeme za vyplnění dotazníku! Vaše odpověď bude pečlivě zpracována a dostanete ve výsledku zašleme Vám na email nabídku setu o kterých jste snili . Do 2 pracovních dnů dostanete na email svůj vysněný set. 
"""
