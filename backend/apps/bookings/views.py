from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookingSerializer


class BookingCreateView(APIView):
    """
    API endpoint for creating new booking requests.
    """

    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save()
            return Response(
                {
                    'success': True,
                    'message': 'Thank you! We will contact you shortly.',
                    'data': BookingSerializer(booking).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'success': False,
                'message': 'Please correct the errors below.',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )
