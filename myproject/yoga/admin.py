from django.contrib import admin
from .models import YogaClass, Booking


@admin.register(YogaClass)
class YogaClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'start_time', 'end_time', 'instructor')
    list_filter = ('date', 'instructor')
    search_fields = ('title', 'description')
    date_hierarchy = 'date'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'yoga_class', 'date_display', 'booked_at')
    list_filter = ('booked_at',)
    search_fields = ('user__username', 'yoga_class__title')

    def date_display(self, obj):
        return obj.yoga_class.date.strftime('%d.%m.%Y')
    date_display.short_description = 'Дата'
