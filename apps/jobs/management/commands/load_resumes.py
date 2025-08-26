import numpy as np
import os
import pandas as pd
from random import choice
from sys import stdout
from weasyprint import HTML
from tqdm import tqdm
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import BaseCommand

from apps.jobs.models import Resume
from apps.jobs.utils import strip_to_lower


FILE_PATH = "hf://datasets/opensporks/resumes/Resume/Resume.csv"
np.random.seed(42)


class Command(BaseCommand):
    help = 'Create random users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of resumes to be created')
        parser.add_argument(
            '--filepath', 
            type=str, 
            help='Path to the directory containing resume files', 
            default=FILE_PATH
        )

    def handle(self, *args, **kwargs):
        """Create random resumes associated with random users"""
        total = kwargs['total']
        filepath = kwargs['filepath']
        
        # Get data and prepare
        df = pd.read_csv(filepath)
        sample_df = df.sample(n=total).reset_index(drop=True)
        sample_df["job_title"] = sample_df["Resume_str"].apply(strip_to_lower, forget_last=2)
        sample_df["Category"] = sample_df["Category"].str.capitalize()
        sample_df["Resume_pdf"] = sample_df["Resume_html"].apply(
            lambda x: HTML(string=x).write_pdf()
        )        
        
        # Get users
        total_created = 0
        users = list(User.objects.all())
        
        # Assign resumes
        resumes = []
        for i, resume_row in tqdm(sample_df.iterrows(), desc="Assigning resumes", unit="resume", file=stdout):
            user = choice(users)
            resume = Resume(
                user=user,
                description=resume_row["Resume_str"][:128],
                job_title=resume_row["job_title"][:64],
                file_name=f"{user.username}_resume_{i}.pdf",
                file=SimpleUploadedFile(
                    name=f"{user.username}_resume_{i}.pdf",
                    content=resume_row["Resume_pdf"],
                    content_type='application/pdf'
                ),
                category=resume_row["Category"],
            )
            resumes.append(resume)
            total_created += 1
        Resume.objects.bulk_create(resumes)            
            
        self.stdout.write(
            self.style.SUCCESS(f"✅ Created {total_created} users.")
        )
