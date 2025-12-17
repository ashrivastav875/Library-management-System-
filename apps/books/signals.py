"""
Books app signals.

Updates search vector after book save for PostgreSQL full-text search.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book


@receiver(post_save, sender=Book)
def update_book_search_vector(sender, instance, created, **kwargs):
    """
    Update the search vector after a book is saved.
    Only runs on PostgreSQL, silently fails on other databases.
    """
    try:
        if not kwargs.get('update_fields') or 'search_vector' not in kwargs.get('update_fields', []):
            instance.update_search_vector()
    except Exception:
        pass  # Silently fail for non-PostgreSQL databases
