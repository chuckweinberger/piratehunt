from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile

class SignUpForm(UserCreationForm):
    username = UsernameField(
                                label='Team Name',
                                widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'})
                            )
    captain = forms.CharField(  max_length=100, 
                                label='Team Captain', 
                                help_text='Please use your real name',
                                widget=forms.TextInput(attrs={'class':'form-control'})
                              )
    email = forms.EmailField(
                                max_length=150, 
                                help_text='Team Captain\'s Email',
                                widget=forms.TextInput(attrs={'class':'form-control'})
                            )
    password1 = forms.CharField(
                                    label="Team Password",
                                    strip=False,
                                    widget=forms.TextInput(attrs={'type':'password','class':'form-control', 'autocomplete': 'new-password'}),
                                    help_text=("Choose a password that you can share with your team")
                                  )
    password2 = forms.CharField(
                                     label="Confirm Password",
                                     strip=False,
                                     widget=forms.TextInput(attrs={'type':'password', 'class':'form-control', 'autocomplete': 'new-password'}),
                                     help_text=("Enter the same password as above for verification"),
                                )
    team_member2 = forms.CharField( max_length=100, 
                                    label='Team Member 1', 
                                    required=False, 
                                    help_text='You can have up to 4 Team Members',
                                    widget=forms.TextInput(attrs={'class':'form-control'})
                                   )
    team_member3 = forms.CharField( max_length=100, 
                                    label='Team Member 2', 
                                    required=False, 
                                    help_text='You can have up to 4 Team Members',
                                    widget=forms.TextInput(attrs={'class':'form-control'})
                                   )
    team_member4 = forms.CharField( max_length=100, 
                                    label='Team Member 3', 
                                    required=False, 
                                    help_text='You can have up to 4 Team Members',
                                    widget=forms.TextInput(attrs={'class':'form-control'})
                                   )
    team_member5 = forms.CharField( max_length=100, 
                                    label='Team Member 4', 
                                    required=False, 
                                    help_text='You can have up to 4 Team Members',
                                    widget=forms.TextInput(attrs={'class':'form-control'})
                                   )

class AnswerForm(forms.Form):
    answer = forms.CharField(label="What\'s your guess?", max_length=400, widget=forms.TextInput(attrs={'class':'form-control'}))
