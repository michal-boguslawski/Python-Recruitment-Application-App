from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# class UserCredentials(models.Model):
#     login = models.CharField(max_length=30, primary_key=True)
#     password = models.CharField(max_length=30)
    
# class UserData(models.Model):
#     first_name = models.CharField(max_length=30)
#     last_name = models.CharField(max_length=30)
#     credential = models.OneToOneField(UserCredentials, on_delete=models.CASCADE)
#     date_of_birth = models.DateField()
#     email = models.EmailField(max_length=200, unique=True)
    
class SocialMediaLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=50)
    link = models.CharField(max_length=100)
    
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    link = models.CharField(max_length=200)
    
class JobPosting(models.Model):
    WORK_MODES = [
    ("onsite", "Onsite"),
    ("remote", "Remote"),
    ("hybrid", "Hybrid"),
    ]
    
    company_name = models.CharField(max_length=100)
    job_position = models.CharField(max_length=50)
    work_mode = models.CharField(max_length=10, choices=WORK_MODES)
    work_location = models.CharField(max_length=100)
    termination_date = models.DateField()
    
class Application(models.Model):
    APPLICATION_STATUSES = [
        ("pending", "Pending"),
        ("interview", "Interview"),
        ("rejected", "Rejected"),
        ("success", "Success"),
    ]

    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    application_status = models.CharField(max_length=10, choices=APPLICATION_STATUSES)


class ApplicationLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    application = models.OneToOneField(Application, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'job_posting')  # Acts like a composite PK

    
class InterviewsDetail(models.Model):
    application = models.ForeignKey(Application, on_delete=models.DO_NOTHING)
    interview_date = models.DateField()
