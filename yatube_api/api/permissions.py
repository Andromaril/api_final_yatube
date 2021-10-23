from rest_framework import permissions


class GetOrPostOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method == "POST" or request.method == "GET":
                return request.method
        return False

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
