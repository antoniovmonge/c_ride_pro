from django.contrib import admin

from c_ride.circles.models import Circle


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

    actions = ["make_verified", "make_unverified"]

    @admin.action(description="Verify selected circles")
    def make_verified(self, request, queryset):
        """Make circles verified."""
        queryset.update(verified=True)

    @admin.action(description="Un-Verify selected circles")
    def make_unverified(self, request, queryset):
        """Make circles verified."""
        queryset.update(verified=False)
