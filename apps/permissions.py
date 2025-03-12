from rest_framework.permissions import BasePermission

from apps.models import User


class IsAdminOrSupperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.user.role == User.Role.ADMIN:
                return True
        return False


class IsOwnerPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user != request.user
        return False

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.user.is_superuser or request.role == User.Role.ADMIN:
                return True
            return True
        return False
