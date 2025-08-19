from django.urls import path
from .views import CustomLoginView, CustomRegisterView, ActivateAccount, CustomLogoutView
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='home:home'), name='logout'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('account_activation_sent/',
         TemplateView.as_view(template_name='users/account_activation_sent.html'),
         name='account_activation_sent'
    ),
]