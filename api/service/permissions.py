from rest_framework import permissions

class IsOwnerPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        return True