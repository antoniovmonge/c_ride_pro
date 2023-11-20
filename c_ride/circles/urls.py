"""Circles URLs."""

# Django
from django.urls import path

from c_ride.circles.views import create_circle, list_circles

app_name = "circles"

urlpatterns = [
    path("", list_circles, name="list_circles"),
    path("create/", create_circle, name="create_circle"),
]
