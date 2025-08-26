from django import template

from apps.users.models import UserProfile
from apps.users.utils import format_phone_number

register = template.Library()

@register.filter
def phone_format(userprofile: UserProfile) -> str:
    """Format the phone number with the country code."""
    return format_phone_number(userprofile.phone_number, userprofile.country)
