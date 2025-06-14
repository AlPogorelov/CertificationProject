from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """
    Разрешает доступ только активным пользователям.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)
