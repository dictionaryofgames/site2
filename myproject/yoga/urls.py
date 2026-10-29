from django.urls import path
from . import views

app_name = 'yoga'

urlpatterns = [
    path('', views.classes_list, name='booking'),
    path('book/<int:class_id>/', views.booking_create, name='book'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.booking_cancel, name='cancel'),
]