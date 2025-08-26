from django.urls import path
from django.shortcuts import render

from .views import ListJobApplicationView, CreateJobApplicationView, jobs_home_view

urlpatterns = [
    path('', jobs_home_view, name='home'),
    path('list/', ListJobApplicationView.as_view(), name='list_of_applications'),
    path('create/', CreateJobApplicationView.as_view(), name='create_application')
]