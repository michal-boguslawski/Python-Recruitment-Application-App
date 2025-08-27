import os
from django.utils import timezone
# from apps.users.models import UserProfile


COUNTRY_DECODER_DICT = {"poland": "PL", "united states": "US", "PL": "PL", "US": "US"}
PHONE_DETAILS_DICT = {
    "PL": {
        "length": 9,
        "prefix": "+48",
        "format": "{prefix} {part1} {part2} {part3}"
    },
    "US": {
        "length": 10,
        "prefix": "+1",
        "format": "{prefix} ({part1}) {part2}-{part3}"
    }
}


def format_phone_number(phone_number: str, country: str = 'poland') -> str:
    """
    Format a phone number according to the rules of the specified country.

    Parameters
    ----------
    phone_number : str
        The raw input phone number, which may contain spaces, dashes,
        or other non-digit characters.
    country : str, optional
        The country for which the phone number should be formatted
        (default is 'poland').

    Returns
    -------
    str
        The formatted phone number as a string.
        If the number does not match expected patterns,
        it may be returned unformatted.
    """
    # Convert PhoneNumber object to string if necessary
    if not isinstance(phone_number, str):
        phone_number = str(phone_number)

    # Normalize country input and get corresponding details
    country_code = COUNTRY_DECODER_DICT.get(country.lower(), 'PL')
    details = PHONE_DETAILS_DICT.get(country_code, PHONE_DETAILS_DICT['PL'])
    prefix = details['prefix']
    number_length = details['length']
    phone_number = phone_number[-number_length:]  # Keep only the last 'length' digits

    # Extract digits from the phone number
    part1 = phone_number[:3]
    part2 = phone_number[3:6]
    part3 = phone_number[6:]
    return details['format'].format(
        prefix=prefix,
        part1=part1,
        part2=part2,
        part3=part3
    )


def user_profile_picture_path(
    instance: "UserProfile",  # type: ignore # noqa: F821
    filename: str
) -> str:
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
