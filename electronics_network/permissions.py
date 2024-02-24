from rest_framework.permissions import BasePermission

class IsOwnerOrSuperuser(BasePermission):
    """ Права только для владельца или суперпользователя """
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner or request.user.is_superuser


class IsActiveAuthenticatedUser(BasePermission):
    """ Права только для активного пользователя """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_active
