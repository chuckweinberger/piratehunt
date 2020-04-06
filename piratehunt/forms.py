from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Team Name',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
