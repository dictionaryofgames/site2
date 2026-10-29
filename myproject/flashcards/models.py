from django.db import models
from django.conf import settings


class Flashcard(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField('Заголовок', max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Флеш-карточка'
        verbose_name_plural = 'Флеш-карточки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class FlashcardItem(models.Model):
    flashcard = models.ForeignKey(Flashcard, related_name='items', on_delete=models.CASCADE)
    front = models.TextField('Лицевая сторона')
    back = models.TextField('Обратная сторона')
    order = models.PositiveIntegerField('Порядок', default=0)

    class Meta:
        verbose_name = 'Элемент флеш-карточки'
        verbose_name_plural = 'Элементы флеш-карточек'
        ordering = ['order']

    def __str__(self):
        return self.front[:50]