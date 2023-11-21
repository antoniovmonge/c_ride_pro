from django.test import Client, TestCase
from django.urls import reverse

from c_ride.circles.models import Circle
from c_ride.circles.serializers import CircleSerializer


class CircleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.list_url = reverse("circles:list_circles")
        self.create_url = reverse("circles:create_circle")

    def test_list_circles(self):
        response = self.client.get(self.list_url)
        circles = Circle.objects.filter(is_public=True)
        serializer = CircleSerializer(circles, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, 200)

    def test_create_circle(self):
        data = {
            "name": "Test Circle",
            "slug_name": "test-circle",
            "about": "This is a test circle",
        }
        response = self.client.post(self.create_url, data)
        circle = Circle.objects.get(name=data["name"])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(circle.name, data["name"])
        self.assertEqual(circle.slug_name, data["slug_name"])
        self.assertEqual(circle.about, data["about"])
