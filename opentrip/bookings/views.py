from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, TemplateView
from bookings.models import Booking, BookedRoom
from hotels.models import RoomType
from bookings.forms import BookingForm
from datetime import datetime

class BookingCreateView(LoginRequiredMixin,CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'bookings/booking_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        room_type_id = self.kwargs.get('room_type_id')
        room_type = get_object_or_404(RoomType, pk=room_type_id)

        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        occupancy = self.request.GET.get('occupancy')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d') if check_in else None
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d') if check_out else None

        context['room_type'] = room_type
        context['check_in'] = check_in
        context['check_out'] = check_out
        context['occupancy'] = occupancy
        context['hotel'] = room_type.hotel
        context['total_price'] = room_type.price_per_night * (check_out_date - check_in_date).days

        return context

    def form_valid(self, form):
        room_type = get_object_or_404(RoomType, pk=self.kwargs['room_type_id'])
        check_in = self.request.GET.get('check_in')
        check_out = self.request.GET.get('check_out')
        occupancy = self.request.GET.get('occupancy')

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d') if check_in else None
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d') if check_out else None

        available_rooms = room_type.get_available_rooms(check_in_date, check_out_date)

        if not available_rooms:
            return redirect('no-available-rooms')

        room = available_rooms.first()

        # Создаем бронирование
        booking = form.save(commit=False)
        booking.user = self.request.user
        booking.room_type = room_type
        booking.save()
        booked_room = BookedRoom.objects.create(
            booking=booking,
            room=room,
            room_type=room_type,
            check_in=check_in_date,
            check_out=check_out_date,
            price=room_type.price_per_night * (check_out_date - check_in_date).days
        )

        return redirect('bookings_app:booking-success')


class SuccessBooking(TemplateView):
    template_name = 'bookings/booking_success.html'

