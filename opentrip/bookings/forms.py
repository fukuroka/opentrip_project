from django import forms
from bookings.models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'surname', 'phone_number', 'email']

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)
