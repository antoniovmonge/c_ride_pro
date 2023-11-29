"""Rides views."""

# Utilities
from datetime import timedelta

# Django REST Framework
from django.utils import timezone
from rest_framework import mixins, viewsets

# Filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated

# Models
from c_ride.circles.models import Circle
from c_ride.circles.permissions.memberships import IsActiveCircleMember
from c_ride.rides.permissions import IsRideOwner

# Serializers
from c_ride.rides.serializers import CreateRideSerializer, RideModelSerializer


class RideViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Ride view set."""

    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ("departure_date", "arrival_date", "available_seats")
    ordering_fields = ("departure_date", "arrival_date", "available_seats")
    search_fields = ("departure_location", "arrival_location")
    # queryset = Ride.objects.filter(is_active=True, available_seats__gte=1)

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ["update", "partial_update"]:
            permissions.append(IsRideOwner)
        return [p() for p in permissions]

    def get_serializer_context(self):
        """Add circle to serializer context."""
        context = super().get_serializer_context()
        context["circle"] = self.circle
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""
        if self.action == "create":
            return CreateRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circle's rides."""
        offset = timezone.now() + timedelta(minutes=10)
        queryset = self.circle.offered_rides.filter(
            departure_date__gte=offset,
            is_active=True,
            available_seats__gte=1,
        )
        return queryset
