"""
Accounts app signals.
Auto-assign users to Members group on registration.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import User


@receiver(post_save, sender=User)
def assign_default_group(sender, instance, created, **kwargs):
    """
    Automatically assign new users to the 'Members' group.
    Administrators must be assigned manually via admin panel.
    """
    if created and not instance.is_superuser:
        members_group, _ = Group.objects.get_or_create(name='Members')
        instance.groups.add(members_group)
