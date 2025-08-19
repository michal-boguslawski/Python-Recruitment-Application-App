from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.generic.edit import FormView

from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
from .models import UserProfile

# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    authentication_form = CustomAuthenticationForm
    
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
