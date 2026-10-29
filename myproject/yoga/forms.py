from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []
        widgets = {
            'yoga_class': forms.Select(attrs={
                'class': 'form-control'
            })
        }