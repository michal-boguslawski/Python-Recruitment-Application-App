# views.py
from django.views import View
from django.shortcuts import render
from .models import ApplicationLink
from .utils import recursive_model_to_dict, explode_dict
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy, reverse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from django.contrib.auth.models import Group

class CustomLoginView(LoginView):
    template_name = 'users/user_login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return self.request.GET.get('next') or reverse('user_applications')
    
class CustomUserChangeForm(UpdateView):
    form_class = UserChangeForm
    template_name = 'users/user_login.html'
    success_url = reverse_lazy('user_applications')  # Or whatever your success url is

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        allowed_fields = ['first_name', 'last_name', 'email']
        for field_name in list(form.fields):
            if field_name not in allowed_fields:
                form.fields.pop(field_name)
        return form
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fill in informations'  # Add extra context here
        return context
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('edit_profile')
    def form_valid(self, form):
        response = super().form_valid(form)
        group = Group.objects.get(name='Customer')
        self.object.groups.add(group)
        return response

    
def home(request):
    return render(request, "home.html")


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


class UserApplicationsListView(ListView):
    model = ApplicationLink
    template_name = 'applications/user_applications.html'
    # context_object_name = 'applications'

    def get_queryset(self):
        return ApplicationLink.objects.filter(user=self.request.user)
