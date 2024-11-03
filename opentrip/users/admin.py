from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CustomerProfile, HotelProfile

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'surname', 'phone_number', 'birthdate')
    list_filter = ('birthdate',)
    search_fields = ('user__username', 'name', 'surname', 'phone_number')

@admin.register(HotelProfile)
class HotelProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'hotel', 'phone_number', 'website')
    search_fields = ('user__username', 'hotel__name', 'phone_number', 'website')