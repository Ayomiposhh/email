from django import forms
from emailapp.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core import validators



class RegForm(UserCreationForm):
    username = forms.CharField(label='Username :', widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': 'Enter Username'}))
    email = forms.EmailField(label='Email :', widget=forms.EmailInput(attrs={'class': 'input-text', 'placeholder': 'Enter Email'}))
    first_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': 'Enter Firstname'}))
    last_name = forms.CharField(required=False, widget=forms.TextInput(
        attrs={'class': 'input-text', 'placeholder': 'Enter Lastname'}))
    password1 = forms.CharField(label='Enter Password :', widget=forms.PasswordInput(
        attrs={'class': 'input-text', 'placeholder': 'Enter Password'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(
        attrs={'class': 'input-text', 'placeholder': 'Enter Password'}))
    botfield = forms.CharField(required=False, widget=forms.HiddenInput(),
                               validators=[validators.MaxLengthValidator(0)])

    def clean_email(self):
        email_field = self.cleaned_data.get('email')
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Email already exist')
        return email_field

    class Meta():
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password1', 'password2']
        