from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from .models import UserProfile, SiteLinks


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

    def clean_username(self):
        username = self.cleaned_data.get('username').lower()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '')
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '')
        return last_name.capitalize()

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number', '')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class CustomUpdateUserForm(UserChangeForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name is None or first_name == '':
            return self.instance.first_name  # keep existing value
        return first_name.capitalize()

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name is None or last_name == '':
            return self.instance.last_name  # keep existing value
        return last_name.capitalize()


class UserProfileUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(required=False)
    country = forms.CharField(required=False)
    city = forms.CharField(required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'country', 'city', 'profile_picture']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number is None or phone_number == '':
            return self.instance.phone_number
        return phone_number

    def clean_country(self):
        country = self.cleaned_data.get('country')
        if country is None or country == '':
            return self.instance.country
        return country

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if city is None or city == '':
            return self.instance.city
        return city


class SiteLinksForm(forms.ModelForm):
    name = forms.CharField(required=True)
    url = forms.URLField(required=True, assume_scheme='https')
    description = forms.CharField(required=False)

    class Meta:
        model = SiteLinks
        fields = ['name', 'url', 'description']
