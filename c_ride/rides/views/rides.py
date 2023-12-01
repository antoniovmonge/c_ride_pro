"""Rides views."""

# Utilities
from datetime import timedelta

from django.utils import timezone

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action

# Filters
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from c_ride.circles.models import Circle
from c_ride.circles.permissions.memberships import IsActiveCircleMember
from c_ride.rides.permissions import IsNotRideOwner, IsRideOwner

# Serializers
from c_ride.rides.serializers import (
    CreateRideSerializer,
    EndRideSerializer,
    JoinRideSerializer,
    RideModelSerializer,
)


class RideViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """Ride view set."""

    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = [SearchFilter, OrderingFilter]
    ordering = ("departure_date", "arrival_date", "available_seats")
    ordering_fields = ("departure_date", "arrival_date", "available_seats")
    search_fields = ("departure_location", "arrival_location")

    def dispatch(self, request, *args, **kwargs):
        """Verify that the circle exists."""
        slug_name = kwargs["slug_name"]
        self.circle = get_object_or_404(Circle, slug_name=slug_name)
        return super().dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ["update", "partial_update", "finish"]:
            permissions.append(IsRideOwner)
        if self.action == "join_ride":
            permissions.append(IsNotRideOwner)
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
        if self.action == "update":
            return JoinRideSerializer
        if self.action == "finish":
            return EndRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """Return active circle's rides."""
        if self.action != "finish":
            offset = timezone.now() + timedelta(minutes=10)
            queryset = self.circle.offered_rides.filter(
                departure_date__gte=offset,
                is_active=True,
                available_seats__gte=1,
            )
            return queryset
        queryset = self.circle.offered_rides.all()
        return queryset

    @action(detail=True, methods=["post"])
    def join_ride(self, request, *args, **kwargs):
        """Add requesting user to ride."""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={"passenger": request.user},
            context={"ride": ride, "circle": self.circle},
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def finish(self, request, *args, **kwargs):
        """Call by owners to finish a ride."""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={"is_active": False, "current_time": timezone.now()},
            context=self.get_serializer_context(),
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)
