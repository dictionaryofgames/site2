from django.db import models
from django.conf import settings
from django.utils import timezone


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

    @staticmethod
    def clean_expired_classes():
        now = timezone.localtime()
        now_time = now.time()
        expired = YogaClass.objects.filter(
            models.Q(date__lt=now.date()) |
            models.Q(date=now.date(), end_time__lte=now_time)
        )
        expired_count = expired.count()
        if expired_count > 0:
            expired.delete()
        return expired_count


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

    @property
    def class_has_passed(self):
        now = timezone.localtime()
        class_datetime = timezone.make_aware(
            timezone.datetime.combine(self.yoga_class.date, self.yoga_class.end_time)
        )
        return now > class_datetime

    @staticmethod
    def clean_expired_bookings():
        now = timezone.localtime()
        now_datetime = timezone.make_aware(
            timezone.datetime.combine(now.date(), now.time())
        )
        expired = Booking.objects.select_related('yoga_class').filter(
            yoga_class__date__lt=now.date()
        )
        expired |= Booking.objects.select_related('yoga_class').filter(
            yoga_class__date=now.date(),
            yoga_class__end_time__lte=now.time()
        )
        expired_count = expired.count()
        if expired_count > 0:
            expired.delete()
        return expired_count