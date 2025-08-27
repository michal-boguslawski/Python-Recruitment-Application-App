from django import forms

from .models import JobApplication, JobApplicationDetails, Resume


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        exclude = ['user']


class JobApplicationDetailsForm(forms.ModelForm):
    new_resume = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'id': 'newResumeInput',
            'style': 'display:none;'
        })
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
