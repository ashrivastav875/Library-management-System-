"""
Ratings app views.

Endpoints for book ratings and reviews.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Avg, Count
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import BookRating
from .serializers import (
    BookRatingSerializer, 
    BookRatingCreateSerializer, 
    BookRatingUpdateSerializer
)
from apps.accounts.permissions import IsOwnerOrAdministrator


class BookRatingViewSet(viewsets.ModelViewSet):
    """
    Book Ratings API
    
    Endpoints for viewing, creating, and managing book ratings.
    
    - **Public**: View ratings
    - **Members**: Create ratings (1 per book)
    - **Owner/Admin**: Update/Delete ratings
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    filter_backends = []
    pagination_class = None

    def get_queryset(self):
        """
        Get ratings queryset with optional book filtering.
        """
        queryset = BookRating.objects.select_related('user', 'book').order_by('-created_at')
        book_id = self.request.query_params.get('book_id')
        if book_id:
            queryset = queryset.filter(book_id=book_id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return BookRatingCreateSerializer
        if self.action in ['update', 'partial_update']:
            return BookRatingUpdateSerializer
        return BookRatingSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrAdministrator()]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_summary="List all ratings",
        operation_description="Get all book ratings. Filter by book with ?book_id=123",
        manual_parameters=[
            openapi.Parameter(
                'book_id', 
                openapi.IN_QUERY, 
                description="Filter by book ID", 
                type=openapi.TYPE_INTEGER, 
                required=False
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Submit a rating",
        operation_description="Add a rating for a book (1 rating per book per user)",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book_id', 'rating'],
            properties={
                'book_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description='Book ID'
                ),
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description='Rating 1-5 stars'
                ),
                'comment': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Review comment (optional)'
                )
            }
        ),
        responses={201: BookRatingSerializer}
    )
    def create(self, request, *args, **kwargs):
        serializer = BookRatingCreateSerializer(
            data=request.data, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        rating = serializer.save()
        return Response(
            BookRatingSerializer(rating).data, 
            status=status.HTTP_201_CREATED
        )

    @swagger_auto_schema(operation_summary="Get rating details")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Update rating",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description='Rating 1-5 stars'
                ),
                'comment': openapi.Schema(
                    type=openapi.TYPE_STRING, 
                    description='Review comment'
                )
            }
        )
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="Delete rating")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="My ratings")
    @action(detail=False, methods=['get'])
    def my_ratings(self, request):
        """Get current user's ratings."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required.'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        queryset = BookRating.objects.filter(
            user=request.user
        ).select_related('book').order_by('-created_at')
        serializer = BookRatingSerializer(queryset, many=True)
        return Response(serializer.data)
