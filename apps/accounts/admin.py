"""
Accounts app admin configuration.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with role-based fields."""
    list_display = ['email', 'username', 'is_administrator', 'is_active', 'created_at']
    list_filter = ['groups', 'is_active', 'is_staff', 'created_at']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-created_at']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Account Info', {
            'fields': ('created_at', 'updated_at'),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']

    def is_administrator(self, obj):
        """Display if user is an administrator."""
        return obj.is_administrator
    is_administrator.boolean = True
    is_administrator.short_description = 'Administrator'
