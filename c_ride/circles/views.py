"""Circle views."""

from django.http import JsonResponse

from c_ride.circles.models import Circle


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
    return JsonResponse(data, safe=False)
