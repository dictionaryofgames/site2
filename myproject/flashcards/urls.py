from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcards_list, name='list'),
    path('create/', views.flashcard_create, name='create'),
    path('<int:pk>/', views.flashcard_detail, name='detail'),
    path('<int:pk>/study/', views.flashcard_study, name='study'),
]