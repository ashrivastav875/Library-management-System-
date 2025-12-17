"""
Books app signals.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book


# No signals needed - simplified model without search vector
