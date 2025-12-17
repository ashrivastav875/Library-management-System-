"""
Custom search backend with PostgreSQL Trigram + Full-Text Search support.
Falls back to basic search if extensions unavailable.
"""
from rest_framework.filters import SearchFilter
from django.db.models import Q, Value, F
from django.conf import settings


def is_postgres():
    """Check if we're using PostgreSQL."""
    db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
    return 'postgresql' in db_engine or 'postgres' in db_engine


class PostgresSearchFilter(SearchFilter):
    """
    Advanced search filter using PostgreSQL Trigram + Full-Text Search.
    Falls back to ILIKE for non-PostgreSQL or when extensions unavailable.
    """
    
    search_param = 'search'
    trigram_threshold = 0.1
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get(self.search_param, '').strip()
        
        if not search_term:
            return queryset
        
        if is_postgres():
            try:
                return self._postgres_search(queryset, search_term, view)
            except Exception:
                # Fall back to basic search if PostgreSQL features fail
                return self._basic_search(queryset, search_term, view)
        else:
            return self._basic_search(queryset, search_term, view)
    
    def _postgres_search(self, queryset, search_term, view):
        """
        PostgreSQL-specific search using Trigram + Full-Text Search.
        """
        from django.contrib.postgres.search import (
            SearchQuery, SearchRank, TrigramSimilarity
        )
        from django.db.models.functions import Greatest
        
        search_query = SearchQuery(search_term, config='english')
        
        # Weighted trigram similarity for different fields
        queryset = queryset.annotate(
            title_sim=TrigramSimilarity('title', search_term),
            author_sim=TrigramSimilarity('author', search_term),
            combined_similarity=Greatest(
                F('title_sim') * 1.5,
                F('author_sim') * 1.3,
            ),
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(
            Q(combined_similarity__gte=self.trigram_threshold) |
            Q(search_vector=search_query) |
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(isbn__icontains=search_term)
        ).order_by('-rank', '-combined_similarity')
        
        return queryset
    
    def _basic_search(self, queryset, search_term, view):
        """
        Fallback basic search using ILIKE.
        """
        return queryset.filter(
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(isbn__icontains=search_term) |
            Q(genre__icontains=search_term) |
            Q(description__icontains=search_term)
        )


class BookSearchFilter(PostgresSearchFilter):
    """
    Specialized search filter for books with weighted field priority.
    """
    pass
