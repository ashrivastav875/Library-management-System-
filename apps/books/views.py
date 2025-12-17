"""
Books app views.
"""
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Book
from .serializers import BookSerializer, BookListSerializer, BookCreateUpdateSerializer
from .filters import BookFilter
from .search import BookSearchFilter
from .ordering import CustomOrderingFilter
from .pagination import CustomPageNumberPagination
from apps.accounts.permissions import IsAdministratorOrReadOnly


class BookViewSet(viewsets.ModelViewSet):
    """
    Library Books API - Search, filter, and browse books
    
    Features:
    - Full-text search with typo tolerance (PostgreSQL trigram)
    - Filter by title, author, genre, availability
    - Sorting and pagination
    """
    
    queryset = Book.objects.all()
    permission_classes = [IsAdministratorOrReadOnly]
    filter_backends = [BookSearchFilter, DjangoFilterBackend, CustomOrderingFilter]
    filterset_class = BookFilter
    search_fields = ['title', 'author', 'description', 'isbn', 'genre']
    ordering_fields = ['title', 'author', 'created_at', 'published_date']
    ordering = ['created_at']
    pagination_class = CustomPageNumberPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return BookCreateUpdateSerializer
        return BookSerializer
    
    @swagger_auto_schema(
        operation_summary="List all books",
        operation_description="Search, filter, sort, and paginate books. Uses PostgreSQL full-text search with typo tolerance.",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search books (fuzzy matching with typo tolerance)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'title',
                openapi.IN_QUERY,
                description="Filter by title",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'author',
                openapi.IN_QUERY,
                description="Filter by author",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'genre',
                openapi.IN_QUERY,
                description="Filter by genre",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'isbn',
                openapi.IN_QUERY,
                description="Filter by ISBN",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'is_available',
                openapi.IN_QUERY,
                description="Filter by availability",
                type=openapi.TYPE_BOOLEAN,
                required=False,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Sort results",
                type=openapi.TYPE_STRING,
                enum=['title_asc', 'title_desc', 'author_asc', 'author_desc', 'created_at_asc', 'created_at_desc'],
                required=False,
            ),
            openapi.Parameter(
                'page',
                openapi.IN_QUERY,
                description="Page number",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=1,
            ),
            openapi.Parameter(
                'page_size',
                openapi.IN_QUERY,
                description="Items per page (max: 100)",
                type=openapi.TYPE_INTEGER,
                required=False,
                default=10,
            ),
        ],
        filter_inspectors=[],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        """Create book and update search vector."""
        book = serializer.save()
        try:
            book.update_search_vector()
        except Exception:
            pass
    
    def perform_update(self, serializer):
        """Update book and refresh search vector."""
        book = serializer.save()
        try:
            book.update_search_vector()
        except Exception:
            pass
