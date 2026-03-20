from django.test import TestCase
from apps.bookings.forms import BookingForm


class BookingFormTest(TestCase):

    def test_valid_form(self):
        form_data = {
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

        form = BookingForm(data=form_data)

        print(form.errors)

        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_fields(self):
        form = BookingForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("name", form.errors)
