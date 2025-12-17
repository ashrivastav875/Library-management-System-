"""
Custom search backend with PostgreSQL Trigram + Full-Text Search support.
Falls back to basic search for non-PostgreSQL databases.
"""
from rest_framework.filters import SearchFilter
from django.db.models import Q, Value, F
from django.db.models.functions import Coalesce
from django.conf import settings


def is_postgres():
    """Check if we're using PostgreSQL."""
    db_engine = settings.DATABASES.get('default', {}).get('ENGINE', '')
    return 'postgresql' in db_engine or 'postgres' in db_engine


class PostgresSearchFilter(SearchFilter):
    """
    Advanced search filter using PostgreSQL Trigram + Full-Text Search.
    
    Features:
    - Trigram similarity for fuzzy matching (handles typos)
    - Full-text search with ranking
    - Combined scoring for best results
    - Falls back to ILIKE for non-PostgreSQL databases
    """
    
    search_param = 'search'
    trigram_threshold = 0.1  # Minimum similarity score (0-1)
    
    def filter_queryset(self, request, queryset, view):
        search_term = request.query_params.get(self.search_param, '').strip()
        
        if not search_term:
            return queryset
        
        # Check if using PostgreSQL
        if is_postgres():
            return self._postgres_search(queryset, search_term, view)
        else:
            # Fall back to basic search for SQLite/other databases
            return self._basic_search(queryset, search_term, view)
    
    def _postgres_search(self, queryset, search_term, view):
        """
        PostgreSQL-specific search using Trigram + Full-Text Search.
        """
        from django.contrib.postgres.search import (
            SearchQuery, SearchRank, TrigramSimilarity, TrigramWordSimilarity
        )
        
        # Create search query for FTS
        search_query = SearchQuery(search_term, config='english')
        
        # Get search fields from view
        search_fields = getattr(view, 'search_fields', ['title', 'author'])
        
        # Build trigram similarity across all fields
        # We use TrigramWordSimilarity for better partial matching
        similarity_expressions = []
        for field in search_fields:
            if field.startswith('^') or field.startswith('=') or field.startswith('@'):
                field = field[1:]  # Remove prefix
            similarity_expressions.append(
                TrigramWordSimilarity(search_term, field)
            )
        
        # Combine similarities (take the max)
        if similarity_expressions:
            from django.db.models.functions import Greatest
            combined_similarity = Greatest(*similarity_expressions)
        else:
            combined_similarity = Value(0)
        
        # Build the query
        queryset = queryset.annotate(
            similarity=combined_similarity,
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(
            Q(similarity__gte=self.trigram_threshold) |
            Q(search_vector=search_query)
        ).order_by('-rank', '-similarity')
        
        return queryset
    
    def _basic_search(self, queryset, search_term, view):
        """
        Fallback basic search using ILIKE (for SQLite/other databases).
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
    Specialized search filter for books with weighted field priority.
    
    Search priority:
    - Title (highest weight)
    - Author (high weight)
    - ISBN (medium weight)
    - Genre (medium weight)
    - Description (lower weight)
    """
    
    def _postgres_search(self, queryset, search_term, view):
        """
        Enhanced book search with custom trigram weights.
        """
        from django.contrib.postgres.search import (
            SearchQuery, SearchRank, TrigramSimilarity
        )
        from django.db.models.functions import Greatest, Coalesce
        
        search_query = SearchQuery(search_term, config='english')
        
        # Weighted trigram similarity for different fields
        queryset = queryset.annotate(
            # Title similarity (most important)
            title_sim=TrigramSimilarity('title', search_term),
            # Author similarity 
            author_sim=TrigramSimilarity('author', search_term),
            # ISBN exact or partial match
            isbn_sim=TrigramSimilarity('isbn', search_term),
            # Genre similarity
            genre_sim=TrigramSimilarity('genre', search_term),
            # Description similarity
            desc_sim=TrigramSimilarity(Coalesce('description', Value('')), search_term),
            # Combined weighted similarity
            combined_similarity=Greatest(
                F('title_sim') * 1.5,  # Title gets 1.5x weight
                F('author_sim') * 1.3,  # Author gets 1.3x weight
                F('isbn_sim') * 1.2,    # ISBN gets 1.2x weight
                F('genre_sim'),
                F('desc_sim') * 0.8     # Description gets 0.8x weight
            ),
            # FTS rank
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(
            Q(combined_similarity__gte=self.trigram_threshold) |
            Q(search_vector=search_query) |
            Q(title__icontains=search_term) |
            Q(author__icontains=search_term) |
            Q(isbn__icontains=search_term)
        ).order_by('-rank', '-combined_similarity')
        
        return queryset
