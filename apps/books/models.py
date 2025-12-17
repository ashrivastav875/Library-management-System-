"""
Books app models.

Core book entity with full-text search support for catalog browsing.
"""
from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Book(models.Model):
    """
    Book model for the catalog inventory.
    
    Supports PostgreSQL full-text search for efficient querying.
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
    
    # PostgreSQL Full-Text Search vector field
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        db_table = 'books'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title', 'author']),
            models.Index(fields=['is_available', 'genre']),
            GinIndex(fields=['search_vector'], name='book_search_vector_idx'),
        ]

    def __str__(self) -> str:
        return f"{self.title} by {self.author}"
    
    def update_search_vector(self) -> None:
        """
        Update the search vector field for full-text search.
        Call this after saving to update the search index.
        """
        from django.db import connection
        
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    UPDATE books SET search_vector = 
                        setweight(to_tsvector('english', COALESCE(title, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(author, '')), 'A') ||
                        setweight(to_tsvector('english', COALESCE(isbn, '')), 'B') ||
                        setweight(to_tsvector('english', COALESCE(genre, '')), 'B') ||
                        setweight(to_tsvector('english', COALESCE(description, '')), 'C')
                    WHERE id = %s
                """, [self.pk])
        except Exception:
            pass  # Silently fail for non-PostgreSQL databases
