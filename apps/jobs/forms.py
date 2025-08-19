from django import forms
from django.utils import timezone

from .models import JobApplication, JobApplicationDetails, Resume


class JobApplicationForm(forms.ModelForm):
    country = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    city = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        choices=JobApplication.STATUS_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    apply_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        initial=timezone.now().date()  # sets today's date by default
    )
    valid_to = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
    )
    class Meta:
        model = JobApplication
        exclude = ['user']

class JobApplicationDetailsForm(forms.ModelForm):
    
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    
    job_application_body = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    
    resume = forms.ChoiceField(
        choices=[], 
        required=False,
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'resumeSelect'})
    )

    new_resume = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'newResumeInput',
            'style': 'display:none;'
        })
    )
    
    salary_range = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = JobApplicationDetails
        exclude = ['job_application']
        
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        if user:
            resumes = Resume.objects.filter(user=user)
            choices = [(r.id, r.description) for r in resumes]
        choices.insert(0, ('upload_new', '➕ Upload new resume'))
        self.fields['resume'].choices = choices
