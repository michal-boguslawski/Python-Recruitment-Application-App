from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from apps.jobs.utils import resume_file_path


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ManyToManyField(User, related_name='job_applications')
    job_name = models.CharField(max_length=64, null=False)
    company = models.CharField(max_length=64, null=False)
    country = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=64, null=True)
    apply_date = models.DateField()
    valid_to = models.DateField()
    portal = models.CharField(max_length=32, null=True)
    link = models.URLField(max_length=128, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='applied')
    
    @property
    def valid_days(self):
        """Return number of days from today until valid_to date"""
        today = timezone.now().date()
        delta = self.valid_to - today
        return delta.days if delta.days >= 0 else 0  # don't return negative
        

class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    description = models.CharField(max_length=128)
    job_title = models.CharField(max_length=64, null=True)
    file_name = models.CharField(max_length=128, null=True, default='')
    file = models.FileField(upload_to=resume_file_path, blank=True, null=True)
    summary = models.TextField(null=True)
    category = models.CharField(
        max_length=64,
        default='',
        # choices=[],
    )
    
    def __str__():
        return Resume.file_name

class JobApplicationDetails(models.Model):
    job_application = models.OneToOneField(JobApplication, on_delete=models.CASCADE, related_name='details')
    resume = models.ManyToManyField(Resume, blank=True, related_name='job_app_details')
    job_application_body = models.TextField(null=True)
    comments = models.TextField(null=True)
    salary_range = models.CharField(max_length=32, null=True)
