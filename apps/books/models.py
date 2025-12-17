"""
Books app models.

Core book entity for catalog browsing.
"""
from django.db import models


class Book(models.Model):
    """
    Book model for the catalog inventory.
    """

    title = models.CharField(max_length=255, db_index=True)
    author = models.CharField(max_length=255, db_index=True)
    isbn = models.CharField(max_length=13, unique=True)
    description = models.TextField(blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    genre = models.CharField(max_length=100, blank=True, db_index=True)
    published_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['is_available', 'genre']),
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
