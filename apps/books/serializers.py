"""
Books app serializers.
"""
from rest_framework import serializers
from .models import Book


class BookSerializer(serializers.ModelSerializer):
    """Full serializer for Book model."""

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn', 'description',
            'page_count', 'genre', 'published_date',
            'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for book listing."""

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author', 'isbn',
            'genre', 'is_available'
        ]


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating and updating books."""

    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'description',
            'page_count', 'genre', 'published_date'
        ]

    def validate_isbn(self, value):
        """Validate ISBN format."""
        # Remove any hyphens or spaces
        isbn = value.replace('-', '').replace(' ', '')
        if len(isbn) not in [10, 13]:
            raise serializers.ValidationError(
                'ISBN must be 10 or 13 characters long.'
            )
        if not isbn.isdigit():
            raise serializers.ValidationError(
                'ISBN must contain only digits.'
            )
        return isbn
