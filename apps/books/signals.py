"""
Books app signals.
Auto-update search vector when books are saved.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book


@receiver(post_save, sender=Book)
def update_book_search_vector(sender, instance, created, **kwargs):
    """
    Update search vector after book save.
    This enables full-text search on PostgreSQL.
    """
    try:
        # Use update() to avoid recursion
        if not kwargs.get('update_fields') or 'search_vector' not in kwargs.get('update_fields', []):
            instance.update_search_vector()
    except Exception:
        # Silently fail for non-PostgreSQL databases
        pass
