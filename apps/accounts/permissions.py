"""
DRF permissions integrated with Django Groups.
"""
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdministrator(BasePermission):
    """
    Allows access only to users in the Administrators group.
    """
    message = 'Only administrators can perform this action.'

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Administrators').exists()
        )


class IsMember(BasePermission):
    """
    Allows access to authenticated members (registered users).
    """
    message = 'You must be a registered member to perform this action.'

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAdministratorOrReadOnly(BasePermission):
    """
    Allows read access to anyone, write access only to Administrators.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return (
            request.user.is_authenticated and
            request.user.groups.filter(name='Administrators').exists()
        )


class IsOwnerOrAdministrator(BasePermission):
    """
    Object-level permission: owner or administrator can access.
    """
    def has_object_permission(self, request, view, obj):
        # Administrators have full access
        if request.user.groups.filter(name='Administrators').exists():
            return True
        # Check if the object belongs to the user
        return hasattr(obj, 'user') and obj.user == request.user
