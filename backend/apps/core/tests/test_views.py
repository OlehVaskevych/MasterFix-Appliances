from django.test import TestCase
from django.urls import reverse
from apps.bookings.models import Booking


class LandingPageViewTest(TestCase):

    def test_booking_create_via_landing_page(self):
        url = reverse("core:landing")

        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "2015550123",
            "address": "Test Address",
            "city": "Lviv",
            "zip_code": "79000",
            "appliance_type": "refrigerator",
            "appliance_brand": "Samsung",
            "appliance_model": "RT38",
            "problem_description": "Not cooling",
        }

        response = self.client.post(url, data, HTTP_USER_AGENT="TestAgent")

        self.assertEqual(response.status_code, 302)  # redirect після success
        self.assertEqual(Booking.objects.count(), 1)
