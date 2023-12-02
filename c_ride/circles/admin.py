"""Circles admin."""

import csv
from datetime import datetime, timedelta

# Django
from django.contrib import admin
from django.http import HttpResponse

# Utilities
from django.utils import timezone

# Models
from c_ride.circles.models import Circle
from c_ride.rides.models import Ride


@admin.register(Circle)
class CircleAdmin(admin.ModelAdmin):
    """Circle admin."""

    list_display = (
        "slug_name",
        "name",
        "is_public",
        "verified",
        "is_limited",
        "members_limit",
    )
    search_fields = ("slug_name", "name")
    list_filter = ("is_public", "verified", "is_limited")

    actions = ["make_verified", "make_unverified", "download_todays_rides"]

    @admin.action(description="Verify selected circles")
    def make_verified(self, request, queryset):
        """Make circles verified."""
        queryset.update(verified=True)

    @admin.action(description="Un-Verify selected circles")
    def make_unverified(self, request, queryset):
        """Make circles verified."""
        queryset.update(verified=False)

    @admin.action(description="Download CSV")
    def download_todays_rides(self, request, queryset):
        """Return a CSV file with today's rides."""
        now = timezone.now()
        start = datetime(now.year, now.month, now.day, 0, 0, 0)
        end = start + timedelta(days=1)
        rides = Ride.objects.filter(
            offered_in__in=queryset.values_list("id"),
            departure_date__gte=start,
            departure_date__lte=end,
        ).order_by("departure_date")
        response = HttpResponse(content_type="text/csv")
        response[
            "Content-Disposition"
        ] = "attachment; filename=todays_rides.csv"
        writer = csv.writer(response)
        writer.writerow(
            [
                "id",
                "offered_in",
                "offered_by",
                "passengers",
                "available_seats",
                "departure_location",
                "departure_date",
                "arrival_location",
                "arrival_date",
                "rating",
            ]
        )
        for ride in rides:
            writer.writerow(
                [
                    ride.pk,
                    ride.offered_in,
                    ride.offered_by,
                    ride.passengers.count(),
                    ride.available_seats,
                    ride.departure_location,
                    str(ride.departure_date),
                    ride.arrival_location,
                    str(ride.arrival_date),
                    ride.rating,
                ]
            )
        return response
