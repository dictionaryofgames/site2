from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import SlotBalance, GameSettings
from .forms import BetForm
import random

# Символы слотов
SLOT_SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
WIN_MULTIPLIERS = {
    '🍒': 2,
    '🍋': 3,
    '🍊': 4,
    '🍇': 5,
    '💎': 10,
    '7️⃣': 20,
}


def get_balance(user):
    balance, created = SlotBalance.objects.get_or_create(user=user)
    if created:
        settings = GameSettings.get_settings()
        balance.balance = settings.initial_balance
        balance.save()
    return balance


def generate_reels():
    settings = GameSettings.get_settings()
    chance = random.randint(1, 100)
    
    if chance <= settings.win_rate_three:
        # Три одинаковых
        symbol = random.choice(SLOT_SYMBOLS)
        return [symbol, symbol, symbol]
    elif chance <= settings.win_rate_three + settings.win_rate_two:
        # Два одинаковых
        symbol = random.choice(SLOT_SYMBOLS)
        other = random.choice([s for s in SLOT_SYMBOLS if s != symbol])
        reels = [symbol, symbol, other]
        random.shuffle(reels)
        return reels
    else:
        # Проигрыш
        symbols = random.sample(SLOT_SYMBOLS, 3)
        return symbols


@login_required
def play(request):
    balance = get_balance(request.user)
    
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = int(form.cleaned_data['bet'])
            
            if balance.spend_coins(bet):
                reels = generate_reels()
                
                # Проверяем выигрыш
                win_amount = 0
                if reels[0] == reels[1] == reels[2]:
                    multiplier = WIN_MULTIPLIERS[reels[0]]
                    win_amount = bet * multiplier
                    balance.add_coins(win_amount)
                elif reels[0] == reels[1] or reels[1] == reels[2] or reels[0] == reels[2]:
                    win_amount = bet // 2
                    balance.add_coins(win_amount)
                
                balance.refresh_from_db()
                
                return render(request, 'slots/play.html', {
                    'reels': reels,
                    'bet': bet,
                    'win_amount': win_amount,
                    'balance': balance.balance,
                    'won': win_amount > 0
                })
            else:
                form.add_error(None, 'Недостаточно монет!')
    else:
        form = BetForm()
    
    return render(request, 'slots/play.html', {
        'form': form,
        'balance': balance.balance,
        'reels': None
    })


@login_required
def add_coins(request):
    """Добавить бесплатные монеты"""
    balance = get_balance(request.user)
    settings = GameSettings.get_settings()
    balance.add_coins(settings.free_coins_amount)
    return redirect('slots:play')