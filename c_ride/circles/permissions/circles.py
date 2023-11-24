# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from c_ride.circles.models import Membership


class IsCircleAdmin(BasePermission):
    """Allow access only to circle admins."""

    def has_object_permission(self, request, view, obj):
        """Verify user have a circle admin permission."""
        try:
            Membership.objects.get(
                user=request.user, circle=obj, is_admin=True, is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True
