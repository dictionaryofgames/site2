from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import YogaClass, Booking
from .forms import BookingForm


def classes_list(request):
    classes = YogaClass.objects.all()
    return render(request, "yoga/classes.html", {"classes": classes})


@login_required
def booking_create(request, class_id):
    yoga_class = get_object_or_404(YogaClass, id=class_id)
    
    if not yoga_class.is_available:
        return render(request, 'yoga/error.html', {
            'message': 'На это занятие нет свободных мест'
        })
    
    if request.method == 'POST':
        if Booking.objects.filter(user=request.user, yoga_class=yoga_class).exists():
            return render(request, 'yoga/booking.html', {
                'yoga_class': yoga_class,
                'message': 'Вы уже забронировали это занятие'
            })
        Booking.objects.create(user=request.user, yoga_class=yoga_class)
        return redirect('yoga:my_bookings')
    
    return render(request, 'yoga/booking.html', {
        'yoga_class': yoga_class
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related("yoga_class")
    return render(request, "yoga/my_bookings.html", {"bookings": bookings})


@login_required
def booking_cancel(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect("yoga:my_bookings")
