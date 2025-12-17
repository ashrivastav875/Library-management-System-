"""
Management command to create a default admin user if it doesn't exist.
"""
from django.core.management.base import BaseCommand
from apps.accounts.models import User


class Command(BaseCommand):
    help = 'Create a default admin user if it does not exist'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Admin username')
        parser.add_argument('--email', type=str, default='admin@example.com', help='Admin email')
        parser.add_argument('--password', type=str, default='admin123', help='Admin password')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'Admin user "{username}" already exists'))
            return

        # Create superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'Successfully created admin user: {username}'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'Email: {email}'
        ))
        self.stdout.write(self.style.WARNING(
            'IMPORTANT: Change the password after first login!'
        ))
