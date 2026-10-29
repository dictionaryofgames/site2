from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flashcard, FlashcardItem
from .forms import FlashcardForm, FlashcardItemForm


@login_required
def flashcards_list(request):
    flashcards = Flashcard.objects.filter(user=request.user)
    return render(request, 'flashcards/list.html', {
        'flashcards': flashcards
    })


@login_required
def flashcard_create(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.save()
            return redirect('flashcards:detail', pk=flashcard.pk)
    else:
        form = FlashcardForm()
    
    return render(request, 'flashcards/create.html', {'form': form})


@login_required
def flashcard_detail(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    items = flashcard.items.all()
    
    if request.method == 'POST':
        if 'add_item' in request.POST:
            form = FlashcardItemForm(request.POST)
            if form.is_valid():
                item = form.save(commit=False)
                item.flashcard = flashcard
                item.order = items.count() + 1
                item.save()
                return redirect('flashcards:detail', pk=flashcard.pk)
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('item_id')
            item = get_object_or_404(FlashcardItem, id=item_id, flashcard=flashcard)
            item.delete()
            return redirect('flashcards:detail', pk=flashcard.pk)
        elif 'delete_flashcard' in request.POST:
            flashcard.delete()
            return redirect('flashcards:list')
    
    form = FlashcardItemForm()
    
    return render(request, 'flashcards/detail.html', {
        'flashcard': flashcard,
        'items': items,
        'form': form
    })


@login_required
def flashcard_study(request, pk):
    flashcard = get_object_or_404(Flashcard, pk=pk, user=request.user)
    items = list(flashcard.items.all())
    
    if not items:
        return render(request, 'flashcards/study.html', {
            'flashcard': flashcard,
            'current_item': None,
            'message': 'Добавьте элементы для изучения'
        })
    
    index = int(request.GET.get('index', 0))
    if index >= len(items):
        index = 0
    
    current_item = items[index]
    next_item = items[(index + 1) % len(items)]
    
    return render(request, 'flashcards/study.html', {
        'flashcard': flashcard,
        'current_item': current_item,
        'next_item': next_item,
        'index': index,
        'total': len(items)
    })