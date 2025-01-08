from rest_framework import permissions

class IsResearcher(permissions.BasePermission):
    """Permission check for researchers."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_researcher

class IsAnalyst(permissions.BasePermission):
    """Permission check for analysts."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_analyst 