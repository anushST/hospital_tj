"""Permissions of the APIs."""
from rest_framework import permissions


class OwnerOrReadOnly(permissions.BasePermission):
    """If owner of the object give access."""

    def has_permission(self, request, view):
        """Check permission on request which doesn't need object."""
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Check permission on request which need object."""
        return (
            True if request.method in permissions.SAFE_METHODS
            else obj.author == request.user
        )
