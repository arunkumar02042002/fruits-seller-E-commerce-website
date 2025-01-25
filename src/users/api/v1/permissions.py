from rest_framework import permissions

class IsCartItemOwner(permissions.BasePermission):
    """Check if the user is the owner of the cart item."""
    def has_object_permission(self, request, view, obj):
        """Check if the user is the owner of the cart item."""
        user = request.user
        ip_address = request.META.get('REMOTE_ADDR')

        if user.is_authenticated:
            return (
                obj.cart.profile is not None and
                obj.cart.profile.user == request.user
            )
        return obj.cart.ip_address == ip_address and obj.cart.profile is None
