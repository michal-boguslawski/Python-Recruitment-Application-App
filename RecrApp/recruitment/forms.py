# forms.py
from django import forms
# from .models import UserCredentials, UserData
from django.contrib.auth.models import User, ApplicationLink, Application


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']
        
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'application_status']

class ApplicationLinkForm(forms.ModelForm):
    class Meta:
        model = ApplicationLink
        fields = ['job_posting']
