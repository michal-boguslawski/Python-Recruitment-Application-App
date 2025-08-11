from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    phone_number = forms.CharField(required=False)
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = (
            "username", "email", "first_name", "last_name", "password1", 
            "password2", "phone_number", "country", "city", "profile_picture"
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                phone_number=self.cleaned_data.get('phone_number', ''),
                country=self.cleaned_data.get('country', ''),
                city=self.cleaned_data.get('city', ''),
                profile_picture=self.cleaned_data.get('profile_picture'),
            )
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'country', 'city', 'profile_picture']
