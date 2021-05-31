from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


class ProductsForm(forms.Form):

    def clean(self):
        cleaned_data = super().clean()
        rc = cleaned_data.get("reibekuchen_count")
        if rc == None:
            rc = 0
        ac = cleaned_data.get("apfelkompott_count")
        if ac == None:
            ac = 0
        lc = cleaned_data.get("lachs_count")
        if lc == None:
            lc = 0
        bc = cleaned_data.get("broetchen_standard_count")
        if bc == None:
            bc = 0
        bsc = cleaned_data.get("broetchen_special_count")
        if bsc == None:
            bsc = 0
        kc = cleaned_data.get("kartoffelsalat_count")
        if kc == None:
            kc = 0
        if rc + ac + lc + bc + bsc + kc == 0:
            raise ValidationError("Bitte mindestens ein Produkt auswählen!")



    reibekuchen_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
        min_value=0
    )

    apfelkompott_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=10,
        min_value=0
    )

    lachs_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=10,
        min_value=0
    )

    broetchen_standard_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
        min_value=0
    )

    broetchen_special_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
        min_value=0
    )

    kartoffelsalat_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
        min_value=0
    )

    wishes = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 5, 'cols': 30}
        ),
        required=False)


class CustomerForm(forms.Form):
    customer_name = forms.CharField(
        widget=forms.TextInput(
            attrs={

            }
        ),
        required=True,
        max_length=100
    )

    callnumber = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'pattern': '[0-9]+',
                'placeholder': 'Format: 02486/1373'
            }
        ),
        required=True,
        max_length=25
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'für die Bestätigungsmail'
            }
        ),
        required=False,
        max_length=75,
    )
