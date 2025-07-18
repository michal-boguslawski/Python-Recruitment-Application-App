# views.py
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import LoginForm, UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# from .models import UserCredentials, UserData

class UserCreateView(View):
    def get(self, request):
        error = None
        form = UserForm()
        # data_form = UserDataForm()
        return render(request, 'users/user_form.html', {
            'form': form,
            'error': error
        })

    def post(self, request):
        error = None
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save()
            # user_data = data_form.save(commit=False)
            # user_data.credential = credentials
            # user_data.save()
            return redirect('user_success')  # Replace with your success URL or view name
        else:
            error = form.errors

        return render(request, 'users/user_form.html', {
            'form': form,
            'error': error
        })

    
def home(request):
    return render(request, "home.html")

def login_view(request):
    error = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                
                return redirect('login_success')  # change 'home' to your success URL
            else:
                error = "Invalid login or password"
    else:
        form = LoginForm()
    
    return render(request, 'users/user_login.html', {'form': form, 'error': error})

def login_success(request):
    print(request.session.keys())
    print(request.session.get('_auth_user_id'))
    print(request.user.username)
    print(request.user.is_authenticated)
    # return render(request, "users/user_login_success.html")
    return redirect('edit_profile')

@login_required
def edit_profile(request):
    user = request.user  # Current logged-in user
    error = None
    if request.method == 'POST':
        print("Post")
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            print("Post2")
            form.save()
            return redirect('home')
        else:
            error = form.errors
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'users/user_form.html', {'form': form, 'error': error, 'title': 'Edit user'})

def user_menu(request):
    pass
    # add new application
    # review applications
    # edit existing application
    # add new resume
    # edit user data

class ApplicationCreateView(View):
    def get(self, request):
        pass

    def post(self, request):
        pass
