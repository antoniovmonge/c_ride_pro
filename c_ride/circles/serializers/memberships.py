"""Membership serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from c_ride.circles.models import Membership

# Serializers
from c_ride.users.serializers import UserModelSerializer


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer."""

    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source="created", read_only=True)

    class Meta:
        """Meta class."""

        model = Membership
        fields = (
            "user",
            "is_admin",
            "is_active",
            "used_invitations",
            "remaining_invitations",
            "rides_taken",
            "rides_offered",
            "joined_at",
            "invited_by",
        )
        read_only_fields = (
            "user",
            "used_invitations",
            "invited_by" "remaining_invitations",
            "rides_taken",
            "rides_offered",
        )
