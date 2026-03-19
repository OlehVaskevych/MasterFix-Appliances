from django.test import TestCase
from apps.bookings.models import Booking


class BookingModelTest(TestCase):

    def test_create_booking(self):
        booking = Booking.objects.create(
            name="John Doe",
            email="john@example.com",
            phone="123456789",
            address="Test Address",
            city="Lviv",
            zip_code="79000",
            appliance_type="refrigerator",
            appliance_brand="Samsung",
            appliance_model="RT38",
            problem_description="Not cooling",
            status="new",
            priority="normal",
        )

        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(booking.name, "John Doe")