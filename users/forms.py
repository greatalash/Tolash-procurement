from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignupForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(label='Username or Phone')
