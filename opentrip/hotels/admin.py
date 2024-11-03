from django.contrib import admin
from .models import Hotel, RoomType, Room, Amenity, HotelImage, RoomImage

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'rating')
    list_filter = ('country', 'city', 'rating')
    search_fields = ('name', 'description', 'address')

@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'occupancy', 'price_per_night')
    list_filter = ('hotel', 'occupancy')
    search_fields = ('name', 'description')


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'number')
    list_filter = ('room_type__hotel', 'room_type')
    search_fields = ('number',)

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)



@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image')
    list_filter = ('hotel',)
    search_fields = ('hotel__name',)

@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room', 'image')
    list_filter = ('room__room_type__hotel', 'room__room_type')
    search_fields = ('room__number',)