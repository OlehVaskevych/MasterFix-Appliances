from django import forms
from phonenumber_field.formfields import PhoneNumberField
from .models import Booking


class BookingForm(forms.ModelForm):
    phone = PhoneNumberField(region="US")

    class Meta:
        model = Booking
        fields = [
            "name",
            "phone",
            "email",
            "appliance_type",
            "appliance_brand",
            "problem_description",
            "zip_code",
        ]

    # === Custom validation ===

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if len(name) < 2:
            raise forms.ValidationError("Name must be at least 2 characters long.")
        return name

    def clean_problem_description(self):
        desc = self.cleaned_data["problem_description"].strip()
        if len(desc) < 10:
            raise forms.ValidationError("Please describe the problem in more detail.")
        return desc

    def clean_zip_code(self):
        zip_code = self.cleaned_data["zip_code"].strip()

        if not zip_code.isdigit():
            raise forms.ValidationError("ZIP code must contain only digits.")

        if len(zip_code) not in [5, 9]:
            raise forms.ValidationError("Enter a valid US ZIP code.")

        return zip_code
