from django.test import TestCase

from c_ride.circles.models import Circle


class CircleModelTestCase(TestCase):
    def setUp(self):
        self.circle = Circle.objects.create(
            name="Test Circle",
            slug_name="test-circle",
            about="This is a test circle",
            rides_offered=5,
            rides_taken=3,
            verified=True,
            is_public=True,
            is_limited=False,
            members_limit=0,
        )

    def test_circle_creation(self):
        self.assertEqual(Circle.objects.count(), 1)
        self.assertEqual(self.circle.name, "Test Circle")
        self.assertEqual(self.circle.slug_name, "test-circle")
        self.assertEqual(self.circle.about, "This is a test circle")
        self.assertEqual(self.circle.rides_offered, 5)
        self.assertEqual(self.circle.rides_taken, 3)
        self.assertEqual(self.circle.verified, True)
        self.assertEqual(self.circle.is_public, True)
        self.assertEqual(self.circle.is_limited, False)
        self.assertEqual(self.circle.members_limit, 0)

    def test_circle_str(self):
        self.assertEqual(str(self.circle), "Test Circle")

    def test_circle_ordering(self):
        self.assertEqual(
            Circle._meta.ordering, ["-rides_taken", "-rides_offered"]
        )
