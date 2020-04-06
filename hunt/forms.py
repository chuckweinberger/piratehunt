from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile

class SignUpForm(UserCreationForm):
        username = UsernameField(
                                    label='Team Name',
                                    widget=forms.TextInput(attrs={'autofocus': True})
                                )
        captain = forms.CharField(max_length=100, label='Team Captain', help_text='Please use your real name')
        team_member2 = forms.CharField(max_length=100, label='Team Member 1', required=False, help_text='You can have up to 4 Team Members')
        team_member3 = forms.CharField(max_length=100, label='Team Member 2', required=False, help_text='You can have up to 4 Team Members')
        team_member4 = forms.CharField(max_length=100, label='Team Member 3', required=False, help_text='You can have up to 4 Team Members')
        team_member5 = forms.CharField(max_length=100, label='Team Member 4', required=False, help_text='You can have up to 4 Team Members')
        email = forms.EmailField(max_length=150, help_text='Team Captain\'s Email')


#
# class UserProfileForm(ModelForm):
#         class Meta:
#                 model = Profile
#                 fields= ["captain", "team_member2", "team_member3", "team_member4", "team_member5"]