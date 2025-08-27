from django.contrib import admin
from .models import JobApplication, Resume, JobApplicationDetails


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ("job_name", "company", "status",
                    "apply_date", "valid_to", "valid_days")
    list_filter = ("status", "company", "country")
    search_fields = ("job_name", "company", "city")
    filter_horizontal = ("user",)


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("description", "job_title", "file_name", "user")
    search_fields = ("description", "job_title", "file_name", "user__username")


@admin.register(JobApplicationDetails)
class JobApplicationDetailsAdmin(admin.ModelAdmin):
    list_display = ("job_application", "salary_range")
    filter_horizontal = ("resume",)
