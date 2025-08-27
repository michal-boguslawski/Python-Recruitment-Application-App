import os
import re
from django.utils import timezone
# from apps.jobs.models import Resume


def to_camel_case(s):
    parts = s.split(' ')  # or split by spaces if needed
    return ' '.join(word.capitalize() for word in parts)


def strip_to_lower(text: str, forget_last: int = 0) -> str:
    """
    Utility function to return leading uppercased characters.

    Args:
        text (str): Input string.
        forget_last (int): Number of characters to forget from the end.
    Returns:
        str: Stripped and lowercased string.
    """
    for i, c in enumerate(text):
        if c.islower():
            substring = text[:(i - forget_last)]
            return to_camel_case(substring)
    text = text.lstrip(" _").rstrip(" _")
    return text


def sanitize_name(s: str) -> str:
    # Replace spaces with underscores
    s = s.replace(" ", "_")
    # Remove non-alphanumeric characters (keep underscores)
    s = re.sub(r"[^\w]", "", s)
    # Collapse multiple underscores into one
    s = re.sub(r"_+", "_", s)
    return s


def resume_file_path(
    instance: "Resume",  # type: ignore # noqa: F821
    filename: str
) -> str:
    """
    Generate file path for new user profile picture:
    MEDIA_ROOT/resumes/<username>_<job_title>_<timestamp>.<ext>

    Args:
        instance (Resume): instance of Resume class
        filename (str): name of uploaded photow
    Returns:
        str: path where the file will be stored with new name
    """
    ext = filename.split('.')[-1]  # get file extension
    timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
    job_title = instance.job_title.replace(' ', '').replace('_', '')

    # Replace spaces and special characters
    sanitized_job_title = sanitize_name(job_title)
    sanitized_username = sanitize_name(instance.user.username)

    filename = f"{sanitized_username}_{sanitized_job_title}_{timestamp}.{ext}"
    return os.path.join('resumes/', filename)
