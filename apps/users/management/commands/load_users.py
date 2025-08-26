from sys import stdout
import os
from tqdm import tqdm
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from media.input_data.generate_data import generate_users
from apps.users.models import UserProfile

class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    def handle(self, *args, **kwargs):
        """Create random users with associated UserProfile"""
        total = kwargs['total']
        users_data = generate_users(total)
        userprofiles = []
        for user_data in tqdm(users_data, desc="Creating users", unit="user", file=stdout):
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
        
        UserProfile.objects.bulk_create(userprofiles)
        total_created = len(userprofiles)
            
        self.stdout.write(
            self.style.SUCCESS(f"✅ Created {total_created} users.")
        )
                