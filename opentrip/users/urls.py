from django.urls import path
from users.views import CustomLoginView,CustomerRegisterView,HotelRegisterView
app_name = 'users_app'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register_user/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register_hotel/', HotelRegisterView.as_view(), name='hotel_register'),
]
