"""Invitations tests."""

# Django
from django.test import TestCase

# Model
from c_ride.circles.models import Circle, Invitation
from c_ride.users.tests.factories import UserFactory


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = UserFactory()
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test-circle",
            about="This is a test circle",
            rides_offered=5,
            rides_taken=3,
            verified=True,
        )

    def test_code_generation(self):
        """Random codes should be generated automatically."""
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        )
        self.assertIsNotNone(invitation.code)

    def test_code_usage(self):
        """If a code is given, there's no need to create a new one."""
        code = "HIXMKL"
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code,
        )
        self.assertEqual(invitation.code, code)

    def test_code_generation_if_duplicated(self):
        """If given code is not unique, a new one must be generated."""
        code = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
        ).code

        # Create another invitation with the past code
        invitation = Invitation.objects.create(
            issued_by=self.user,
            circle=self.circle,
            code=code,
        )
        self.assertNotEqual(code, invitation.code)
