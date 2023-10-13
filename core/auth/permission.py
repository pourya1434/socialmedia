from rest_framework.permissions import BasePermission, SAFE_METHODS

# SAFE_METHODS => GET, OPTIONS, HEAD

class UserPermission(BasePermission):
    # list and detail view
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return request.method in SAFE_METHODS
        if view.basename in ['post']:
            return bool(request.user and request.user.is_authenticated)
        
        return False
    # list
    def has_permission(self, request, view):
        if view.basename in ['post']:
            if request.user.is_anonymous:
                return request.method in SAFE_METHODS
            return bool(request.user and request.user.is_authenticated)
        return False