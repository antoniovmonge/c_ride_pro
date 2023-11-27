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


class IsSelfMember(BasePermission):
    """Allow access only to member owners."""

    def has_permission(self, request, view):
        """Let object permission grant access."""
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Verify user is the owner of the member object."""
        return request.user == obj.user
