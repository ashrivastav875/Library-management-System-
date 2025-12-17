"""
Management command to create default groups with permissions.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType


class Command(BaseCommand):
    help = 'Create default groups (Administrators and Members) with appropriate permissions'

    def handle(self, *args, **options):
        self.stdout.write('Setting up groups and permissions...')

        # Create Administrators group
        admin_group, created = Group.objects.get_or_create(name='Administrators')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Administrators group'))
        else:
            self.stdout.write('Administrators group already exists')

        # Create Members group
        members_group, created = Group.objects.get_or_create(name='Members')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Members group'))
        else:
            self.stdout.write('Members group already exists')

        # Get content types for our models
        try:
            from apps.books.models import Book
            from apps.loans.models import Loan
            from apps.reviews.models import Review

            book_ct = ContentType.objects.get_for_model(Book)
            loan_ct = ContentType.objects.get_for_model(Loan)
            review_ct = ContentType.objects.get_for_model(Review)

            # Administrators get all permissions for books, loans, and reviews
            admin_permissions = Permission.objects.filter(
                content_type__in=[book_ct, loan_ct, review_ct]
            )
            admin_group.permissions.set(admin_permissions)
            self.stdout.write(f'Assigned {admin_permissions.count()} permissions to Administrators')

            # Members can view books and manage their own loans and reviews
            member_permissions = Permission.objects.filter(
                content_type=book_ct,
                codename='view_book'
            ) | Permission.objects.filter(
                content_type=loan_ct,
                codename__in=['add_loan', 'view_loan']
            ) | Permission.objects.filter(
                content_type=review_ct,
                codename__in=['add_review', 'view_review', 'change_review', 'delete_review']
            )
            members_group.permissions.set(member_permissions)
            self.stdout.write(f'Assigned {member_permissions.count()} permissions to Members')

        except Exception as e:
            self.stdout.write(self.style.WARNING(
                f'Could not assign model permissions: {e}. '
                'Run migrations first, then run this command again.'
            ))

        self.stdout.write(self.style.SUCCESS('Groups setup completed!'))
