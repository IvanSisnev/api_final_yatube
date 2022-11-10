"""
Кастомные пермишен классы для api.
"""
from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """
    Кастомный пермишен класс для разграничения доступа user/author vs. anon.
    """
    def has_permission(self, request, view):
        """Определяет возможность запроса."""
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        """Определяет права доступа к объекту."""
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
