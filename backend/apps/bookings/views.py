from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

# DRF
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BookingSerializer


# === API (для Vue / AJAX) ===
class BookingCreateView(APIView):
    def post(self, request):
        serializer = BookingSerializer(data=request.data)

        if serializer.is_valid():
            booking = serializer.save(
                ip_address=request.META.get("REMOTE_ADDR"),
                user_agent=request.META.get("HTTP_USER_AGENT"),
            )

            return Response(
                {
                    "success": True,
                    "message": "Thank you! We will contact you shortly.",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
