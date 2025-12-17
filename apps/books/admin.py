"""
Books app admin configuration.
"""
from django.contrib import admin
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """Admin configuration for Book model."""
    list_display = ['title', 'author', 'isbn', 'genre', 'is_available', 'created_at']
    list_filter = ['is_available', 'genre', 'created_at']
    search_fields = ['title', 'author', 'isbn', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'isbn')
        }),
        ('Details', {
            'fields': ('description', 'page_count', 'genre', 'published_date')
        }),
        ('Status', {
            'fields': ('is_available',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
