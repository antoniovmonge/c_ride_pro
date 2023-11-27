"""Circle views."""

# Django
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

# Django REST Framework
from rest_framework import mixins, viewsets

# Filters
from rest_framework.filters import OrderingFilter, SearchFilter
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
    lookup_field = "slug_name"

    # Filters
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    search_fields = ("slug_name", "name")
    ordering_fields = (
        "rides_offered",
        "rides_taken",
        "name",
        "created",
        "members_limit",
    )
    # ordering = ("-members_count", "-rides_offered", "-rides_taken")
    filter_fields = ("verified", "is_limited")

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all().annotate(members_count=Count("members"))
        if self.action == "list":
            return queryset.filter(is_public=True).order_by(
                "-members_count", "-rides_offered", "-rides_taken"
            )
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
