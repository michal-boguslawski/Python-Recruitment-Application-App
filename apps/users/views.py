from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic import DetailView, UpdateView
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, UserProfileForm, CustomUpdateUserForm, UserProfileUpdateForm, SiteLinksForm
from .models import UserProfile, SiteLinks

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = AuthenticationForm
    
    def get_success_url(self):
        return reverse_lazy('jobs:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your custom context variables here
        context['title'] = 'Please Log In'
        context['button_info'] = 'Log In'
        return context
    
class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('home:home')
    
    def get_success_url(self):
        return reverse_lazy('home:home')
    

class CustomRegisterView(FormView):
    form_class = CustomUserCreationForm
    second_form_class = UserProfileForm
    redirect_authenticated_user = True
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:account_activation_sent')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your custom context variables here
        context['title'] = 'Please Register'
        context['button_info'] = 'Register'
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            UserProfile.objects.create(
                user=user,
                phone_number=form.cleaned_data.get('phone_number', ''),
                country=form.cleaned_data.get('country', ''),
                city=form.cleaned_data.get('city', ''),
                profile_picture=form.cleaned_data.get('profile_picture'),
            )
            
            # Send activation email (your existing code)
            current_site = get_current_site(request)
            mail_subject = 'Activate your account'
            message = render_to_string('users/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            EmailMessage(mail_subject, message, to=[user.email]).send()

            return redirect(self.success_url)
        
        return self.render_to_response(
            self.get_context_data(form=form)
        )

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            # Optional: login user here
            return redirect('users:login')
        else:
            return render(request, 'users/activation_invalid.html')

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add your custom context variables here
        
        profile = self.request.user.userprofile
        site_links = self.request.user.sitelinks.all()
        context['site_links'] = site_links
        context['profile'] = profile
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/update_profile.html'
    model = User
    form_class = CustomUpdateUserForm
    second_form_class = UserProfileUpdateForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_formset_class(self):
        return modelformset_factory(
            SiteLinks,
            form=SiteLinksForm,
            extra=0,
            can_delete=True
        )
        
    def get_formset(self):
        FormsetClass = self.get_formset_class()
        if self.request.method == "POST":
            return FormsetClass(self.request.POST, queryset=self.get_queryset())
        return FormsetClass(queryset=self.get_queryset())

    def get_queryset(self):
        return self.request.user.sitelinks.all()

    def get_second_form(self):
        if self.request.method == "POST":
            return self.second_form_class(self.request.POST, self.request.FILES, instance=self.request.user.userprofile)
        return self.second_form_class(instance=self.request.user.userprofile)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["second_form"] = kwargs.get("second_form", self.get_second_form())
        context["formset"] = kwargs.get("formset", self.get_formset())
        return context

    def post(self, request, *args, **kwargs):
        self.get_object()  # Ensure we have the user object
        form = self.get_form()
        second_form = self.get_second_form()
        formset = self.get_formset()

        if form.is_valid() and second_form.is_valid() and formset.is_valid():
            # Save user form
            form.save()

            # Save user profile form
            second_form.save()
            
            instances = formset.save(commit=False)
            for obj in instances:
                obj.user = self.request.user
                obj.save()
            # delete objects if marked
            for obj in formset.deleted_objects:
                obj.delete()
            return redirect(self.get_success_url())
        return self.render_to_response(
            self.get_context_data(form=form, second_form=second_form, formset=formset)
        )
