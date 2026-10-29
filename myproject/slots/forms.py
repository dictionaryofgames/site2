from django import forms


class BetForm(forms.Form):
    BET_CHOICES = [
        (10, 10),
        (50, 50),
        (100, 100),
        (500, 500),
        (1000, 1000),
    ]
    bet = forms.ChoiceField(choices=BET_CHOICES, label='Ставка')