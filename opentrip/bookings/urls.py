from django.urls import path
from bookings.views import BookingCreateView,SuccessBooking, UserBookingsView
app_name = 'bookings_app'

urlpatterns = [
    path('booking_<int:room_type_id>/', BookingCreateView.as_view(), name='booking-create'),
    path('success_booking/', SuccessBooking.as_view(), name = 'booking-success'),
    path('user-bookings/', UserBookingsView.as_view(), name='user-bookings'),
]
