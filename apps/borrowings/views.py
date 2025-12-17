"""
Borrowings app views.

Handles book checkout, checkin, and borrowing history endpoints.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi
from .models import Borrowing
from .serializers import (
    BorrowingSerializer, 
    BorrowingDetailSerializer, 
    CheckoutBookSerializer, 
    EmptySerializer
)
from apps.books.models import Book
from apps.accounts.permissions import IsAdministrator, IsOwnerOrAdministrator


class BorrowingViewSet(viewsets.ModelViewSet):
    """
    Book Borrowing Management API
    
    Endpoints for checking out books, viewing borrowing history,
    and processing returns.
    
    - **Members**: Checkout books, view own borrowings
    - **Administrators**: View all borrowings, process checkins
    """
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']
    filter_backends = []
    pagination_class = None

    def get_queryset(self):
        """
        Filter borrowings based on user role.
        
        Members see only their own borrowings.
        Administrators see all borrowings.
        """
        user = self.request.user
        queryset = Borrowing.objects.select_related('user', 'book')
        
        if getattr(self, 'swagger_fake_view', False):
            return Borrowing.objects.none()
        
        if user.groups.filter(name='Administrators').exists():
            return queryset.order_by('-borrowed_at')
        return queryset.filter(user=user).order_by('-borrowed_at')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BorrowingDetailSerializer
        return BorrowingSerializer

    @swagger_auto_schema(
        operation_summary="List borrowings",
        operation_description="""
**Administrators**: View all borrowings in the system  
**Members**: View only your own borrowings
        """,
        responses={200: BorrowingSerializer(many=True)},
        manual_parameters=[]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get borrowing details",
        operation_description="Retrieve details of a specific borrowing by ID"
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Checkout a book",
        operation_description="Checkout a book by its ID. Users can only have 1 active borrowing at a time.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['book_id'],
            properties={
                'book_id': openapi.Schema(
                    type=openapi.TYPE_INTEGER, 
                    description='ID of the book to checkout'
                )
            }
        ),
        responses={
            201: BorrowingSerializer,
            400: "Book not available or borrowing limit reached"
        }
    )
    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Checkout a book by ID."""
        serializer = CheckoutBookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        book_id = serializer.validated_data['book_id']

        with transaction.atomic():
            try:
                book = Book.objects.select_for_update().get(pk=book_id)
            except Book.DoesNotExist:
                return Response(
                    {'error': 'Book not found.'}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            if not book.is_available:
                return Response(
                    {'error': 'Book is not available.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if user already has this book
            if Borrowing.objects.filter(
                user=request.user, 
                book=book, 
                returned_at__isnull=True
            ).exists():
                return Response(
                    {'error': 'You already have this book checked out.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Enforce 1-book limit per user
            if Borrowing.objects.filter(
                user=request.user, 
                returned_at__isnull=True
            ).exists():
                return Response(
                    {'error': 'You can only have 1 book checked out at a time.'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            borrowing = Borrowing.objects.create(user=request.user, book=book)
            book.is_available = False
            book.save()

        return Response(BorrowingSerializer(borrowing).data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="Checkin a book",
        operation_description="Process a book return by borrowing ID. Requires administrator access.",
        request_body=no_body,
        responses={
            200: BorrowingSerializer,
            400: "Book already returned",
            404: "Borrowing not found"
        }
    )
    @action(detail=True, methods=['post'], permission_classes=[IsAdministrator])
    def checkin(self, request, pk=None):
        """Process a book return (Admin only)."""
        borrowing = self.get_object()

        if borrowing.returned_at:
            return Response(
                {'error': 'Book already returned.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            borrowing.returned_at = timezone.now()
            borrowing.save()
            borrowing.book.is_available = True
            borrowing.book.save()

        return Response(BorrowingSerializer(borrowing).data)

    @swagger_auto_schema(
        operation_summary="Current borrowings",
        operation_description="""
Get your currently active (unreturned) borrowings.

**Note**: The 'id' field is the BORROWING ID - use this for checkin!
        """
    )
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get active borrowings."""
        queryset = self.get_queryset().filter(returned_at__isnull=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="All borrowings (Admin)",
        operation_description="View all borrowings in the system - requires administrator access"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrator])
    def all_records(self, request):
        """Get all borrowings in the system (Admin only)."""
        queryset = Borrowing.objects.select_related('user', 'book').order_by('-borrowed_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Overdue borrowings (Admin)",
        operation_description="Get all overdue borrowings - requires administrator access"
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAdministrator])
    def overdue(self, request):
        """Get overdue borrowings (Admin only)."""
        queryset = Borrowing.objects.filter(
            returned_at__isnull=True,
            due_date__lt=timezone.now()
        ).select_related('user', 'book').order_by('-due_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="My borrowing history",
        operation_description="Get all your borrowings including returned books"
    )
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get current user's complete borrowing history."""
        queryset = Borrowing.objects.filter(
            user=request.user
        ).select_related('book').order_by('-borrowed_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
