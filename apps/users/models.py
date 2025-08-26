import os
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField


def user_profile_picture_path(instance: "UserProfile", filename: str) -> str:
    """
    Generate file path for new user profile picture:
    MEDIA_ROOT/profile_pics/<username>_<timestamp>.<ext>
    
    Args:
        instance (UserProfile): instance of UserProfile class
        filename (str): name of uploaded photow
    Returns:
        str: path where the file will be stored with new name
    """
    ext = filename.split('.')[-1]  # get file extension
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    filename = f"{instance.user.username}_{timestamp}.{ext}"
    return os.path.join('profile_pics/', filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone_number = PhoneNumberField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class SiteLinks(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sitelinks')
    name = models.CharField(max_length=50)
    url = models.URLField(max_length=200)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
