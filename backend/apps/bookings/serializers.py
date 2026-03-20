from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model with validation.
    """

    phone = PhoneNumberField(region="US")

    class Meta:
        model = Booking
        fields = ["id", "name", "phone", "problem_description", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        attrs["name"] = attrs["name"].strip()
        attrs["problem_description"] = attrs["problem_description"].strip()
        return attrs

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError(
                "Please enter a valid name (at least 2 characters)."
            )

        if not value.replace(" ", "").isalpha():
            raise serializers.ValidationError("Name should contain only letters.")

        return value

    def validate_problem_description(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Please provide a more detailed description (at least 10 characters)."
            )

        if len(value) > 500:
            raise serializers.ValidationError(
                "Description is too long (max 500 characters)."
            )

        return value
