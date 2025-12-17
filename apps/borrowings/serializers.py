"""
Borrowings app serializers.

Handles serialization for book checkout and return operations.
"""
from rest_framework import serializers
from .models import Borrowing
from apps.books.serializers import BookListSerializer
from apps.books.models import Book


class BorrowingSerializer(serializers.ModelSerializer):
    """Serializer for Borrowing model with computed fields."""

    book = BookListSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'id', 'user_email', 'book', 'borrowed_at',
            'due_date', 'returned_at', 'is_active', 'is_overdue'
        ]
        read_only_fields = ['id', 'borrowed_at', 'returned_at']


class BorrowingDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single borrowing view."""

    book = BookListSerializer(read_only=True)
    user_email = serializers.EmailField(source='user.email', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Borrowing
        fields = [
            'id', 'user_email', 'user_username', 'book', 'borrowed_at',
            'due_date', 'returned_at', 'is_active', 'is_overdue'
        ]


class CheckoutBookSerializer(serializers.Serializer):
    """Serializer for checking out a book."""

    book_id = serializers.IntegerField(help_text='ID of the book to checkout')

    def validate_book_id(self, value: int) -> int:
        try:
            book = Book.objects.get(pk=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError('Book not found.')

        if not book.is_available:
            raise serializers.ValidationError('Book is not available for checkout.')

        return value


class EmptySerializer(serializers.Serializer):
    """Empty serializer for endpoints that don't need a request body."""
    pass
