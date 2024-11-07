from django import forms
from .models import Hotel, HotelImage

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name','address', 'city', 'country', 'description', 'check_in_time', 'check_out_time', 'rating', 'preview',]
        widgets = {
            'check_in_time': forms.TimeInput(format='%H:%M'),
            'check_out_time': forms.TimeInput(format='%H:%M'),
        }
