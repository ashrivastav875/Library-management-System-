"""
Accounts app models.

Extended User model with Django Groups integration for role-based access.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended User model for the catalog system.
    
    Uses Django Groups for role-based access control:
    - Administrators: Full CRUD access to books, manage users, view all borrowings
    - Members: Browse books, checkout/return books, manage own profile
    """
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    @property
    def is_administrator(self) -> bool:
        """Check if user belongs to Administrators group."""
        return self.groups.filter(name='Administrators').exists()

    @property
    def is_member(self) -> bool:
        """Check if user belongs to Members group."""
        return self.groups.filter(name='Members').exists()

    def __str__(self) -> str:
        return self.email
