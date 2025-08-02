from rest_framework import permissions


class IsStaffUser(permissions.BasePermission):
    """Custom permission to allow only staff users to create, update, and delete."""

    def has_permission(self, request, view):
        # Allow read-only actions for all authenticated users
        if view.action in ["list", "retrieve"]:
            return request.user and request.user.is_authenticated
        # Allow create, update, and delete actions only for staff users
        return request.user and request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow any authenticated user to list or retrieve objects,
    but only the owner of the object can create, update, or delete.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only actions for all authenticated users
        if view.action in ["list", "retrieve"]:
            return True
        # Allow create, update, and delete actions only for the owner of the object
        return request.user == obj.user
