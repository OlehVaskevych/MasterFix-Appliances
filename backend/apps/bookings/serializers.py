from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for Booking model with validation.
    """
    phone = PhoneNumberField(region='US')

    class Meta:
        model = Booking
        fields = ['id', 'name', 'phone', 'problem_description', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_name(self, value):
        """Validate name field."""
        if len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Name must be at least 2 characters long."
            )
        return value.strip()

    def validate_problem_description(self, value):
        """Validate problem description field."""
        if len(value.strip()) < 10:
            raise serializers.ValidationError(
                "Please provide a more detailed description (at least 10 characters)."
            )
        return value.strip()
