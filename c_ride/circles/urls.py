"""Circles URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from c_ride.circles.views import circles as circle_views

app_name = "circles"

router = DefaultRouter()
router.register(
    r"",
    circle_views.CircleViewSet,
    basename="circle",
)


urlpatterns = [
    path("", include((router.urls, app_name))),
]
