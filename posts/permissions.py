from rest_framework import permissions


class PermissionPost(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user == obj.poster or request.user.is_staff:
                return True
            elif request.method in permissions.SAFE_METHODS:
                return True
            else:
                return False