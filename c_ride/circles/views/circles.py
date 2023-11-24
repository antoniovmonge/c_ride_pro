"""Circle views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

# Models
from c_ride.circles.models import Circle, Membership

# Permissions
from c_ride.circles.permissions import IsCircleAdmin

# Serializers
from c_ride.circles.serializers import CircleModelSerializer


class CircleViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Circle view set."""

    serializer_class = CircleModelSerializer

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated]
        if self.action in ["update", "partial_update"]:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin."""
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10,
        )
