"""Circle views."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from c_ride.circles.models import Circle
from c_ride.circles.serializers import CircleSerializer, CreateCircleSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def list_circles(request):
    """List existing circles."""
    public_circles = Circle.objects.filter(is_public=True)
    serializer = CircleSerializer(public_circles, many=True)
    data = serializer.data
    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_circle(request):
    serializer = CreateCircleSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    circle = serializer.save()
    return Response(CircleSerializer(circle).data)
