from rest_framework import permissions

# Custom permission class to allow only the user themselves to modify their own object
class IsSelfOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allowing safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Allowing the user to modify their own object, denying access if the object doesn't belong to the user
        return obj == request.user  # Checks if the object being accessed matches the requesting user
