# configuration/management/commands/createsuperuser_if_not_exists.py

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    """
    Creates a superuser non-interactively if one does not already exist.
    Requires SUPERUSER_USERNAME, SUPERUSER_EMAIL, and SUPERUSER_PASSWORD 
    to be set as environment variables.
    """
    help = 'Creates a superuser non-interactively if one does not already exist.'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # 1. Get credentials from environment variables
        username = os.environ.get('SUPERUSER_USERNAME')
        email = os.environ.get('SUPERUSER_EMAIL')
        password = os.environ.get('SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.WARNING(
                'Skipping superuser creation: SUPERUSER_USERNAME, SUPERUSER_EMAIL, or SUPERUSER_PASSWORD not set.'
            ))
            return

        # 2. Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.SUCCESS(
                f'Superuser "{username}" already exists.'
            ))
            return

        # 3. Create the superuser
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser: {username}'
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Failed to create superuser: {e}'
            ))