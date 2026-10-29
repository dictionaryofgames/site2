from django.db import models
from django.conf import settings


class GameSettings(models.Model):
    win_rate_three = models.PositiveIntegerField(
        'Шанс 3 одинаковых (%)',
        default=10,
        help_text='Вероятность выпадения 3 одинаковых символов'
    )
    win_rate_two = models.PositiveIntegerField(
        'Шанс 2 одинаковых (%)',
        default=30,
        help_text='Вероятность выпадения 2 одинаковых символов'
    )
    initial_balance = models.PositiveIntegerField(
        'Начальный баланс',
        default=10000
    )
    free_coins_amount = models.PositiveIntegerField(
        'Количество бесплатных монет',
        default=5000
    )

    class Meta:
        verbose_name = 'Настройки игры'
        verbose_name_plural = 'Настройки игры'

    def __str__(self):
        return 'Настройки слотов'

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class SlotBalance(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField('Баланс', default=10000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}: {self.balance} монет"

    def add_coins(self, amount):
        self.balance += amount
        self.save()

    def spend_coins(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False