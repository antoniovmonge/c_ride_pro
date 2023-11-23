"""Circle views."""

# Django REST Framework
from rest_framework import viewsets

# Models
from c_ride.circles.models import Circle

# Serializers
from c_ride.circles.serializers import CircleModelSerializer


class CircleViewSet(viewsets.ModelViewSet):
    """Circle view set."""

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
