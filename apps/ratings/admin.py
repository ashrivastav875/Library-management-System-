"""
Ratings app admin configuration.
"""
from django.contrib import admin
from .models import BookRating


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    """Admin configuration for BookRating model."""
    
    list_display = ['user', 'book', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__email', 'user__username', 'book__title', 'comment']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    autocomplete_fields = ['user', 'book']
    list_per_page = 25
