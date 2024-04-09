from django import forms
from .models import RequestConsultation
from phonenumber_field.formfields import PhoneNumberField


class ConsultationForm(forms.ModelForm):
    name = forms.CharField(
        label='',
        error_messages={'required': ''},
        required=True,
        widget=forms.TextInput(attrs={'class': 'cons_form', 'placeholder': 'Фамилия и имя'}),
    )
    age = forms.IntegerField(
        label='',
        error_messages={'required': ''},
        required=True,
        widget=forms.NumberInput(attrs={'class': 'cons_form', 'placeholder': 'Ваш возраст'})
    )
    email = forms.EmailField(
        label='',
        error_messages={'required': ''},
        required=True,
        widget=forms.TextInput(attrs={'class': 'cons_form', 'placeholder': 'Email'})
    )
    phone = PhoneNumberField(
        label='',
        error_messages={'required': ''},
        required=True,
        widget=forms.TextInput(attrs={'class': 'cons_form', 'placeholder': 'Номер телефона'})
    )
    country = forms.CharField(
        label='',
        error_messages={'required': ''},
        required=True,
        widget=forms.TextInput(attrs={'class': 'cons_form', 'placeholder': 'Страна проживания'})
    )

    class Meta:
        model = RequestConsultation
        fields = ['name', 'age', 'email', 'phone', 'country']