"""
Ratings app serializers.

Handles serialization for book ratings and reviews.
"""
from rest_framework import serializers
from .models import BookRating
from apps.books.models import Book


class BookRatingSerializer(serializers.ModelSerializer):
    """Book rating output serializer."""
    
    user_email = serializers.EmailField(source='user.email', read_only=True)
    book_title = serializers.CharField(source='book.title', read_only=True)

    class Meta:
        model = BookRating
        fields = [
            'id', 'user_email', 'book', 'book_title', 
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user_email', 'book_title', 'created_at']


class BookRatingCreateSerializer(serializers.Serializer):
    """Serializer for creating a book rating."""
    
    book_id = serializers.IntegerField(help_text="ID of the book to rate")
    rating = serializers.IntegerField(
        min_value=1, 
        max_value=5, 
        help_text="Rating from 1 to 5 stars"
    )
    comment = serializers.CharField(
        required=False, 
        allow_blank=True, 
        help_text="Optional review comment"
    )

    def validate_book_id(self, value: int) -> int:
        """Ensure book exists."""
        if not Book.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Book not found.')
        return value

    def validate(self, attrs: dict) -> dict:
        """Ensure user hasn't already rated this book."""
        request = self.context.get('request')
        if request and request.user:
            if BookRating.objects.filter(
                user=request.user, 
                book_id=attrs['book_id']
            ).exists():
                raise serializers.ValidationError({
                    'book_id': 'You have already rated this book.'
                })
        return attrs

    def create(self, validated_data: dict) -> BookRating:
        """Create rating with current user."""
        book = Book.objects.get(pk=validated_data['book_id'])
        return BookRating.objects.create(
            user=self.context['request'].user,
            book=book,
            rating=validated_data['rating'],
            comment=validated_data.get('comment', '')
        )


class BookRatingUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating a book rating."""
    
    class Meta:
        model = BookRating
        fields = ['rating', 'comment']
