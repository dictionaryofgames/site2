from django import forms
from .models import Flashcard, FlashcardItem


class FlashcardForm(forms.ModelForm):
    class Meta:
        model = Flashcard
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название карточки'
            })
        }


class FlashcardItemForm(forms.ModelForm):
    class Meta:
        model = FlashcardItem
        fields = ['front', 'back']
        widgets = {
            'front': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Вопрос/Термин'
            }),
            'back': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ответ/Определение'
            }),
            
             
        }