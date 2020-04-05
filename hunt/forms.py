from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=100, help_text='Team Name')
    # first_name = forms.CharField(max_length=100, help_text='First Name')
    # last_name = forms.CharField(max_length=100, help_text='Last Name')
    email = forms.EmailField(max_length=150, help_text='Team Captain\'s Email')

class Meta:
    model = User
    fields = ( 'username', 'email', 'password1', 'password2')
