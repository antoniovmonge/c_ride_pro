"""Invitations tests."""

# Django
from django.test import TestCase

# Django REST Framework
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Model
from c_ride.circles.models import Circle, Invitation, Membership
from c_ride.users.models import Profile

# Factories
from c_ride.users.tests.factories import UserFactory


class InvitationsManagerTestCase(TestCase):
    """Invitations manager test case."""

    def setUp(self):
        """Test case setup."""
        self.user = UserFactory()
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test_circle",
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


class MemberInvitationsAPITestCase(APITestCase):
    """Member invitations API test case."""

    def setUp(self):
        """Test case setup."""
        self.user = UserFactory()
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test_circle",
            about="This is a test circle",
            rides_offered=5,
            rides_taken=3,
            verified=True,
        )
        self.profile = Profile.objects.create(user=self.user)
        self.membership = Membership.objects.create(
            user=self.user,
            profile=self.user.profile,
            circle=self.circle,
            remaining_invitations=10,
        )

        # Auth
        self.token = Token.objects.create(user=self.user).key
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

        # URL
        self.url = f"/circles/{self.circle.slug_name}/members/{self.user.name}/invitations/"

    def test_response_success(self):
        """Verify request succeed."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invitation_creation(self):
        """Verify invitations are generated if none exist previously."""
        # Invitations in DB must be 0
        self.assertEqual(Invitation.objects.count(), 0)

        # Call member invitations endpoint
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new invitations were generated
        invitations = Invitation.objects.filter(issued_by=self.user)
        self.assertEqual(
            invitations.count(), self.membership.remaining_invitations
        )
        for invitation in invitations:
            self.assertIn(invitation.code, response.data["invitations"])
