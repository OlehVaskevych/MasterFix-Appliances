from django.urls import path
from .views import BookingCreateView

app_name = 'bookings'

urlpatterns = [
    path('', BookingCreateView.as_view(), name='create'),
]
