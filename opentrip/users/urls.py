from django.urls import path
from users.views import CustomLoginView,CustomerRegisterView,HotelRegisterView,CustomLogoutView,LogoutTemplateView,ProfileView
app_name = 'users_app'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register_user/', CustomerRegisterView.as_view(), name='customer_register'),
    path('register_hotel/', HotelRegisterView.as_view(), name='hotel_register'),
    path('logout/', CustomLogoutView.as_view(next_page='users_app:logout-success'), name='logout'),
    path('logout_success', LogoutTemplateView.as_view(),name = 'logout-success'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
