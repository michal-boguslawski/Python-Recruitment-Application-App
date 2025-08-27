from django.contrib import admin
from .models import UserProfile, SiteLinks


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "country", "city")
    search_fields = ("user__username", "phone_number", "country", "city")


@admin.register(SiteLinks)
class SiteLinksAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "url", "description")
    search_fields = ("user__username", "name", "url")
    list_filter = ("user",)
