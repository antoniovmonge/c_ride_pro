"""Rides models."""

# Django
from django.db import models

# Utilities
from c_ride.utils.models import CRideModel


class Ride(CRideModel):
    """Ride model."""

    offered_by = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Ride offered by user",
        related_name="offered_rides",
    )

    offered_in = models.ForeignKey(
        "circles.Circle",
        on_delete=models.SET_NULL,
        null=True,
        help_text="Circle in which the ride is offered",
        related_name="offered_rides",
    )

    passengers = models.ManyToManyField(
        "users.User",
        help_text="Passengers that have joined the ride",
        related_name="passengers",
    )

    available_seats = models.PositiveSmallIntegerField(
        default=1, help_text="Number of available seats on the ride"
    )

    comments = models.TextField(blank=True)

    departure_location = models.CharField(max_length=255)
    departure_date = models.DateTimeField()
    arrival_location = models.CharField(max_length=255)
    arrival_date = models.DateTimeField()

    rating = models.FloatField(null=True, help_text="Ride rating")

    is_active = models.BooleanField(
        "active status",
        default=True,
        help_text="Used for disabling the ride or marking it as finished",
    )

    def __str__(self):
        """Return ride details."""
        return (
            f"{str(self.departure_location)} to "
            f"{str(self.arrival_location)} | "
            f"{self.departure_date.strftime('%a %d, %b')} - "
            f"{self.departure_date.strftime('%I:%M %p')} "
            f"{self.arrival_date.strftime('%I:%M %p')}"
        )
