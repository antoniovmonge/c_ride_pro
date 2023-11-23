"""Circle views."""

# Django REST Framework
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# Models
from c_ride.circles.models import Circle

# Serializers
from c_ride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Restrict list to public-only."""
        queryset = Circle.objects.all()
        if self.action == "list":
            return queryset.filter(is_public=True)
        return queryset
