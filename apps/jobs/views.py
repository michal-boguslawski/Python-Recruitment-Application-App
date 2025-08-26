from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .models import JobApplication, Resume
from .forms import JobApplicationForm, JobApplicationDetailsForm

class ListJobApplicationView(LoginRequiredMixin, ListView):
    template_name = 'jobs/list_of_applications.html'
    model = JobApplication
    paginate_by = 20
    login_url = '/users/login/'   # redirect if not logged in
    redirect_field_name = 'next'  # (default, can omit)

    def get_queryset(self):
        sort_by = self.request.GET.get("sort", "apply_date")
        order = self.request.GET.get("order", "desc")
        sort_field = f"-{sort_by}" if order == "desc" else sort_by
        return JobApplication.objects.filter(user=self.request.user).order_by(sort_field)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sort_by"] = self.request.GET.get("sort", "apply_date")
        context["order"] = self.request.GET.get("order", "desc")
        return context
    
class CreateJobApplicationView(LoginRequiredMixin, FormView):
    template_name = "jobs/create_application.html"
    form_class = JobApplicationForm
    second_form_class = JobApplicationDetailsForm
    login_url = '/users/login/'   # redirect if not logged in
    redirect_field_name = 'next'  # (default, can omit)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add second form to context for template rendering
        if 'second_form' not in context:
            context['second_form'] = self.second_form_class(user=self.request.user)
            context['resumes'] = user=self.request.user.resumes.all()
        return context

    def get_success_url(self):
        return reverse_lazy('jobs:list_of_applications')
    
    def form_valid(self, form):
        # Save the object without committing to DB yet
        job_app = form.save(commit=False)
        job_app.save()  # Save the job application first

        # Add the logged-in user
        job_app.user.add(self.request.user)

        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            profile = self.request.user.userprofile
            if profile:
                initial['country'] = profile.country
                initial['city'] = profile.city
                initial['apply_date'] = timezone.now().date()
        return initial

    def post(self, request, *args, **kwargs):
        # Bind both forms with POST data
        self.object = None
        form = self.form_class(request.POST)
        second_form = self.second_form_class(request.POST, request.FILES, user=request.user)
        if form.is_valid() and second_form.is_valid():
            return self.forms_valid(form, second_form)
        else:
            return self.form_invalid(form)

    def forms_valid(self, form, second_form):
        job_app = form.save(commit=False)
        job_app.save()
        job_app.user.add(self.request.user)

        job_details = second_form.save(commit=False)
        job_details.job_application = job_app

        # Handle new resume upload
        new_file = second_form.cleaned_data.get('new_resume')
        if new_file:
            resume = Resume.objects.create(
                user=self.request.user,
                description=new_file.name,
                file=new_file
            )
            job_details.resume = resume
        else:
            resume_id = second_form.cleaned_data.get('resume')
            if resume_id and resume_id != 'upload_new':
                job_details.resume = Resume.objects.get(id=resume_id)

        job_details.save()
        return super().form_valid(form)

def jobs_home_view(request):
    return render(request, template_name='jobs/home.html')
