"""Circles URLs."""

# Django
from django.urls import path

from c_ride.circles.views import list_circles

app_name = "circles"

urlpatterns = [
    path("", list_circles, name="list_circles"),
]
