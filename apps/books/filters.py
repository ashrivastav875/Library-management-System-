"""
Books app filters.
"""
import django_filters
from .models import Book


class BookFilter(django_filters.FilterSet):
    """Filter for book listing with search capabilities."""

    title = django_filters.CharFilter(lookup_expr='icontains')
    author = django_filters.CharFilter(lookup_expr='icontains')
    genre = django_filters.CharFilter(lookup_expr='icontains')
    isbn = django_filters.CharFilter(lookup_expr='exact')
    published_year = django_filters.NumberFilter(
        field_name='published_date',
        lookup_expr='year'
    )
    is_available = django_filters.BooleanFilter()

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'isbn', 'is_available']
