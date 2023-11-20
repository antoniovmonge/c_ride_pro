"""Circle views."""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from c_ride.circles.models import Circle


@api_view(["GET"])
@permission_classes([AllowAny])
def list_circles(request):
    """List existing circles."""
    public_circles = Circle.objects.filter(is_public=True)
    data = []
    for circle in public_circles:
        data.append(
            {
                "name": circle.name,
                "slug_name": circle.slug_name,
                "rides_offered": circle.rides_offered,
                "rides_taken": circle.rides_taken,
                "verified": circle.verified,
                "is_limited": circle.is_limited,
                "members_limit": circle.members_limit,
            }
        )
    return Response(data)


@api_view(["POST"])
@permission_classes([AllowAny])
def create_circle(request):
    name = request.data["name"]
    slug_name = request.data["slug_name"]
    about = request.data.get("about", "")

    circle = Circle.objects.create(
        name=name,
        slug_name=slug_name,
        about=about,
    )
    data = {
        "name": circle.name,
        "slug_name": circle.slug_name,
        "rides_offered": circle.rides_offered,
        "rides_taken": circle.rides_taken,
        "verified": circle.verified,
        "is_limited": circle.is_limited,
        "members_limit": circle.members_limit,
    }
    return Response(data)
