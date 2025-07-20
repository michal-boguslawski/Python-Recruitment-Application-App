# views.py
from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from .forms import LoginForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Application, ApplicationLink
from .utils import recursive_model_to_dict, explode_dict

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
            # authentication using email
            return redirect('home')  # Replace with your success URL or view name
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
                
                return redirect('edit_profile')  # change 'home' to your success URL
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
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
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
    
class ListApplicationsView(View):
    def get(self, request):
        # user = request.user
        error = None
        # get_context_data
        application_links = ApplicationLink.objects.select_related(
            'user', 'job_posting', 'application'
        ).all()
        app_dict = [explode_dict(recursive_model_to_dict(obj)) for obj in application_links]
        
        return render(request, 'recr_app/applications.html', {'info': app_dict, 'error': error})
    
def test(request):
    return render(request, 'recr_app/recr_app_base.html')
