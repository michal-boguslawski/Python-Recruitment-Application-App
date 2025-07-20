from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='user_create'),
    path('login/', views.login_view, name='user_login'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('', views.home, name='home'),
    path('test/', views.ListApplicationsView.as_view(), name='test'),
]