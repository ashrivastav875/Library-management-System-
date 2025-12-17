"""
Borrowings app admin configuration.
"""
from django.contrib import admin
from .models import Borrowing


@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    """Admin configuration for Borrowing model."""
    
    list_display = [
        'user', 
        'book', 
        'borrowed_at', 
        'due_date', 
        'returned_at', 
        'borrowing_status'
    ]
    list_filter = ['returned_at', 'due_date', 'borrowed_at']
    search_fields = ['user__email', 'user__username', 'book__title', 'book__isbn']
    readonly_fields = ['borrowed_at']
    ordering = ['-borrowed_at']
    autocomplete_fields = ['user', 'book']
    date_hierarchy = 'borrowed_at'
    list_per_page = 25

    @admin.display(description='Status')
    def borrowing_status(self, obj) -> str:
        """Display borrowing status."""
        if obj.returned_at:
            return 'Returned'
        elif obj.is_overdue:
            return 'Overdue'
        return 'Active'
