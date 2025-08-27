import os
from sys import stdout
from tqdm import tqdm
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from media.input_data.generate_data import generate_users
from apps.users.models import UserProfile, SiteLinks


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument(
            'total',
            type=int,
            help='Indicates the number of users to be created'
        )

    def handle(self, *args, **kwargs):
        """Create random users with associated UserProfile"""
        total = kwargs['total']
        users_data = generate_users(total)
        userprofiles = []
        userlinks = []
        for user_data in tqdm(
            users_data,
            desc="Creating users",
            unit="user",
            file=stdout
        ):
            # Create User
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                password=user_data['password'],
                is_active=True,
            )

            if user:
                # Create UserProfile
                profile_picture_path = user_data.get('profile_picture')
                image_file = SimpleUploadedFile(
                    name=os.path.basename(profile_picture_path),
                    content=open(profile_picture_path, 'rb').read(),
                    content_type='image/jpeg'
                ) if profile_picture_path else None

                userprofile = UserProfile(
                    user=user,
                    phone_number=user_data.get('phone_number', ''),
                    country=user_data.get('country', ''),
                    city=user_data.get('city', ''),
                    profile_picture=image_file
                )
                userprofiles.append(userprofile)

                # Create SiteLinks
                for site in ['linkedIn', 'github']:
                    url_key = f"{site}_url"
                    if user_data.get(url_key):
                        site_links_data = SiteLinks(
                            user=user,
                            name=site.capitalize(),
                            url=user_data[url_key],
                            description=f"User's {site.capitalize()} profile"
                        )
                        userlinks.append(site_links_data)

        UserProfile.objects.bulk_create(userprofiles)
        SiteLinks.objects.bulk_create(userlinks)
        total_created = len(userprofiles)

        self.stdout.write(
            self.style.SUCCESS(f"✅ Created {total_created} users.")
        )
