from django.contrib import admin
from .models import Booking, BookedRoom

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking_reference', 'created_at', 'total_price', 'status')
    list_filter = ('status', 'created_at')
    search_fields = ('user__user__username', 'booking_reference')

@admin.register(BookedRoom)
class BookedRoomAdmin(admin.ModelAdmin):
    list_display = ('booking', 'room', 'check_in', 'check_out', 'price')
    list_filter = ('booking__status', 'room__room_type__hotel', 'check_in', 'check_out')
    search_fields = ('booking__booking_reference', 'room__number')