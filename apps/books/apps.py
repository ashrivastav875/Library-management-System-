"""
Books app configuration.
"""
from django.apps import AppConfig


class BooksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.books'
    verbose_name = 'Books'

    def ready(self):
        """Import signals when app is ready."""
        import apps.books.signals  # noqa: F401
