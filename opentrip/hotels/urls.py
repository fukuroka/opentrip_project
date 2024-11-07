from django.urls import path
from .views import SearchHotelsView, HotelRoomTypesView, HotelCreateView

app_name = 'hotels_app'

urlpatterns = [
    path('hotels/', SearchHotelsView.as_view(), name = 'search_hotels'),
    path('rooms_<int:pk>', HotelRoomTypesView.as_view(), name = 'hotel_types_room'),
    path('create_hotel/', HotelCreateView.as_view(), name='create_hotel'),
]
