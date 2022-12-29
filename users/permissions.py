from rest_framework import permissions


class MyPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_object_permission(self, request, view, obj):
        if obj.id != request.user.id and not request.user.is_admin and request.user.id != 1:
            return False
        else:
            return True
