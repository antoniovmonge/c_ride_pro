"""Membership permissions."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from c_ride.circles.models import Membership


class IsActiveCircleMember(BasePermission):
    """Allow access only to circle members.

    Expect that views implementing this permission
    have a `circle` attribute assigned.
    """

    def has_permission(self, request, view):
        """Verify user is an active member of the circle."""
        try:
            Membership.objects.get(
                user=request.user, circle=view.circle, is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True

        # Alternative solution
        # return request.user in view.circle.members.all()
