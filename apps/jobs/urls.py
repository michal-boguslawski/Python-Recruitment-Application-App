from django.urls import path
from django.shortcuts import render

from .views import ListJobApplicationView, CreateJobApplicationView

urlpatterns = [
    path('', lambda request: render(request, template_name='jobs/home.html'), name='home'),
    path('list/', ListJobApplicationView.as_view(), name='list_of_applications'),
    path('create/', CreateJobApplicationView.as_view(), name='create_application')
]