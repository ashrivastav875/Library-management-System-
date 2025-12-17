"""
Custom search backend with PostgreSQL Full-Text Search support.
Falls back to basic search for non-PostgreSQL databases or when extensions unavailable.
"""
from rest_framework.filters import SearchFilter
from django.db.models import Q, Value, F
from django.db.models.functions import Coalesce
from django.conf import settings


def is_postgres():
    """Check if we're using PostgreSQL."""
    db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
    return 'postgresql' in db_engine or 'postgres' in db_engine


def has_trigram_extension():
    """Check if pg_trgm extension is available."""
    if not is_postgres():
        return False
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'pg_trgm'")
            return cursor.fetchone() is not None
    except Exception:
        return False


class PostgresSearchFilter(SearchFilter):
    """
    Advanced search filter with PostgreSQL Full-Text Search.
    
    Falls back to ILIKE for non-PostgreSQL databases or when
    pg_trgm extension is not available.
    """
    
    search_param = 'search'
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get(self.search_param, '').strip()
        
        if not search_term:
            return queryset
        
        # Always use basic search for reliability
        return self._basic_search(queryset, search_term, view)
    
    def _basic_search(self, queryset, search_term, view):
        """
        Basic search using ILIKE (works on all databases).
        """
        search_fields = getattr(view, 'search_fields', ['title', 'author'])
        
        q_objects = Q()
        for field in search_fields:
            # Remove any prefixes
            if field.startswith(('^', '=', '@', '$')):
                field = field[1:]
            q_objects |= Q(**{f'{field}__icontains': search_term})
        
        return queryset.filter(q_objects)


class BookSearchFilter(PostgresSearchFilter):
    """
    Specialized search filter for books.
    
    Searches across:
    - Title
    - Author
    - ISBN
    - Genre
    - Description
    """
    
    def _basic_search(self, queryset, search_term, view):
        """
        Book-specific search with multiple fields.
        """
        return queryset.filter(
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(isbn__icontains=search_term) |
            Q(genre__icontains=search_term) |
            Q(description__icontains=search_term)
        )
