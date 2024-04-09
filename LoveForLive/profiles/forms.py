import phonenumber_field.widgets
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.formfields import PhoneNumberField
from .models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={'class': 'auth_form_input', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        label='',
        widget=forms.PasswordInput(attrs={'class': 'auth_form_input', 'placeholder': 'Введите пароль'})
    )

    class Meta:
        model = User
        fields = ['username', 'password']


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'reg_form_input', 'placeholder': 'Введите логин'})
    )
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'reg_form_input', 'placeholder': 'Введите Email'})
    )
    password1 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'reg_form_input', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'reg_form_input', 'placeholder': 'Повторно введите логин'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    phone = PhoneNumberField(
        label='',
        widget=phonenumber_field.widgets.RegionalPhoneNumberWidget(attrs={'class': 'profile_form_input', 'placeholder': 'Введите номер телефона'})
    )

    class Meta:
        model = Profile
        fields = ['phone']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'profile_form_input', 'placeholder': 'Введите Email'})
    )

    class Meta:
        model = User
        fields = ['email']