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
        "circles/<slug:slug_name>/",
        ride_views.RideViewSet.as_view({"post": "create"}),
        name="ride_list",
    ),
]
