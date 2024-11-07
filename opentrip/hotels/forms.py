from django import forms
from .models import Hotel, Review

class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['name','address', 'city', 'country', 'description', 'check_in_time', 'check_out_time', 'rating', 'preview',]
        widgets = {
            'check_in_time': forms.TimeInput(format='%H:%M'),
            'check_out_time': forms.TimeInput(format='%H:%M'),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
