from rest_framework import permissions

class IsAuthenticated(permissions.BasePermission):
    """
    Разрешение, требующее аутентификации пользователя.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
class IsModerator(permissions.BasePermission):
    """
    Разрешение, требующее, чтобы пользователь был модератором.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_moderator
