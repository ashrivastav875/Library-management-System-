"""
Ratings app models.

Handles book ratings and reviews from users.
"""
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class BookRating(models.Model):
    """
    User ratings and reviews for books.
    
    Each user can rate a book once with a 1-5 star rating
    and an optional text review.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='book_ratings',
        help_text='User who submitted the rating'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='ratings',
        help_text='Book being rated'
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Rating from 1 to 5 stars'
    )
    comment = models.TextField(
        blank=True,
        help_text='Optional review text'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'book_ratings'
        unique_together = ['user', 'book']
        ordering = ['-created_at']
        verbose_name = 'Book Rating'
        verbose_name_plural = 'Book Ratings'

    def __str__(self) -> str:
        return f"{self.user.email} - {self.book.title} ({self.rating}/5)"
