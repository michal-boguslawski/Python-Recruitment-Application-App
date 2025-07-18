from django.apps import AppConfig
from django.db.models.signals import post_migrate

def create_default_groups(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import SocialMediaLink, Resume, JobPosting, Application, ApplicationLink, InterviewsDetail
    group, created = Group.objects.get_or_create(name='Customer')
    for model in [SocialMediaLink, Resume, JobPosting, Application, ApplicationLink, InterviewsDetail]:
        content_type = ContentType.objects.get_for_model(model)

        permissions = Permission.objects.filter(
            content_type=content_type,
        )

        group.permissions.add(*permissions) 

class RecruitmentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recruitment'
    
    def ready(self):
        # Connect signal here
        post_migrate.connect(create_default_groups, sender=self)
