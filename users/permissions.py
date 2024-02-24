from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """ Разрешения для модели пользователей."""
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        elif request.user and request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
            # Разрешить доступ к остальным действиям только админу
            return True
        return False
