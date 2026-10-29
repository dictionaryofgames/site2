from django.db import models
from django.conf import settings


class YogaClass(models.Model):
    title = models.CharField('Название занятия', max_length=200)
    description = models.TextField('Описание', blank=True)
    date = models.DateField('Дата занятия')
    start_time = models.TimeField('Время начала')
    end_time = models.TimeField('Время окончания')
    max_participants = models.PositiveIntegerField('Максимум участников', default=10)
    instructor = models.CharField('Преподаватель', max_length=100)

    class Meta:
        verbose_name = 'Занятие йоги'
        verbose_name_plural = 'Занятия йоги'
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%d.%m.%Y')} ({self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')})"

    @property
    def available_spots(self):
        booked = self.bookings.count()
        return self.max_participants - booked

    @property
    def is_available(self):
        return self.available_spots > 0


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    yoga_class = models.ForeignKey(YogaClass, related_name='bookings', on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
        unique_together = ['user', 'yoga_class']

    def __str__(self):
        return f"{self.user.username} - {self.yoga_class.title}"