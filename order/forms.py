from django import forms
from django.core.validators import validate_email


class ProductsForm(forms.Form):
    reibekuchen_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=True,
        max_value=20,
        min_value=1
    )

    apfelkompott_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
        min_value=0
    )

    lachs_count = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control-sm'}
        ),
        required=False,
        max_value=20,
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
        min_value=1
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
