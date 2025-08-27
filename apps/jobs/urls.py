from django.urls import path

from .views import ListJobApplicationView, CreateJobApplicationView, jobs_home_view, \
    ResumeListView

urlpatterns = [
    path('', jobs_home_view, name='home'),
    path('list/', ListJobApplicationView.as_view(), name='list_of_applications'),
    path('create/', CreateJobApplicationView.as_view(), name='create_application'),
    path('resume_list/', ResumeListView.as_view(), name='resume_list'),
]
