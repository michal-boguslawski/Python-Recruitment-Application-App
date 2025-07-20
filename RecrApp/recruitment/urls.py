from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='user_create'),
    path('login/', views.CustomLoginView.as_view(), name='user_login'),
    path('edit_profile/', views.CustomUserChangeForm.as_view(), name='edit_profile'),
    path('', views.home, name='home'),
    path('app/', views.UserApplicationsListView.as_view(), name='user_applications'),
]