"""
Borrowings app models.

Handles book checkout and return functionality with due date tracking.
"""
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class Borrowing(models.Model):
    """
    Tracks book checkouts by users.
    
    Records when a user borrows a book, the due date,
    and when (if) the book was returned.
    """

    DEFAULT_BORROWING_DAYS = 14

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='borrowings',
        help_text='User who borrowed the book'
    )
    book = models.ForeignKey(
        'books.Book',
        on_delete=models.CASCADE,
        related_name='borrowings',
        help_text='Book that was borrowed'
    )
    borrowed_at = models.DateTimeField(
        auto_now_add=True,
        help_text='When the book was checked out'
    )
    due_date = models.DateTimeField(
        help_text='When the book should be returned'
    )
    returned_at = models.DateTimeField(
        null=True, 
        blank=True,
        help_text='When the book was checked in (null if still borrowed)'
    )

    class Meta:
        db_table = 'borrowings'
        ordering = ['-borrowed_at']
        verbose_name = 'Borrowing'
        verbose_name_plural = 'Borrowings'
        indexes = [
            models.Index(fields=['user', 'returned_at']),
            models.Index(fields=['book', 'returned_at']),
        ]

    def save(self, *args, **kwargs):
        """Set default due_date if not provided."""
        if not self.due_date:
            self.due_date = timezone.now() + timedelta(days=self.DEFAULT_BORROWING_DAYS)
        super().save(*args, **kwargs)

    def clean(self):
        """Validate that the book is available for borrowing."""
        if not self.pk and self.book and not self.book.is_available:
            raise ValidationError('This book is not available for borrowing.')

    @property
    def is_active(self) -> bool:
        """Check if borrowing is currently active (not returned)."""
        return self.returned_at is None

    @property
    def is_overdue(self) -> bool:
        """Check if borrowing is overdue."""
        if self.returned_at:
            return False
        return timezone.now() > self.due_date

    def __str__(self) -> str:
        status = 'Active' if self.is_active else 'Returned'
        return f"{self.user.email} - {self.book.title} ({status})"
