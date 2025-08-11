from django.urls import path
from .views import jobs_home

urlpatterns = [
    path('', jobs_home, name='home'),
]