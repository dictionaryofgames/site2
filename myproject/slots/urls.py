from django.urls import path
from . import views

app_name = 'slots'

urlpatterns = [
    path('', views.play, name='play'),
    path('add-coins/', views.add_coins, name='add_coins'),
]