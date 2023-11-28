"""Rides views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated

from c_ride.circles.models import Circle
from c_ride.circles.permissions.memberships import IsActiveCircleMember

# Models
from c_ride.rides.models import Ride

# Serializers
from c_ride.rides.serializers import CreateRideSerializer


class RideViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """Ride view set."""

    serializer_class = CreateRideSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    queryset = Ride.objects.filter(is_active=True, available_seats__gte=1)

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super().get_serializer_context()
        context["circle"] = self.circle
        return context
