"""Rides URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import rides as ride_views

app_name = "rides"

router = DefaultRouter()
router.register(
    r"",
    ride_views.RideViewSet,
    basename="ride",
)

urlpatterns = [
    path("", include((router.urls, app_name))),
    path(
        "circles/<slug:slug_name>/rides/",
        ride_views.RideViewSet.as_view({"get": "list", "post": "create"}),
        name="ride_list",
    ),
    path(
        "circles/<slug:slug_name>/rides/<pk>/",
        ride_views.RideViewSet.as_view(
            {
                "put": "update",
                "patch": "partial_update",
                "get": "retrieve",
            }
        ),
    ),
    path(
        "circles/<slug:slug_name>/rides/<pk>/join/",
        ride_views.RideViewSet.as_view({"post": "join_ride"}),
        name="ride_join",
    ),
    path(
        "circles/<slug:slug_name>/rides/<pk>/finish/",
        ride_views.RideViewSet.as_view({"post": "finish"}),
        name="ride_finish",
    ),
    path(
        "circles/<slug:slug_name>/rides/<pk>/ratings/",
        ride_views.RideViewSet.as_view({"post": "rate"}),
        name="ride_rate",
    ),
]
