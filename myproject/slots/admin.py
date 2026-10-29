from django.contrib import admin
from .models import GameSettings, SlotBalance


@admin.register(GameSettings)
class GameSettingsAdmin(admin.ModelAdmin):
    list_display = ('win_rate_three', 'win_rate_two', 'initial_balance', 'free_coins_amount')
    fields = ('win_rate_three', 'win_rate_two', 'initial_balance', 'free_coins_amount')


@admin.register(SlotBalance)
class SlotBalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)
