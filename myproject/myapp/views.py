from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm


def home_view(request):
    return render(request, 'myapp/home.html', {
        'user': request.user
    })
    
def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    
    return render(request, 'myapp/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home') 
    else:
        form = RegisterForm()
    
    return render(request, 'myapp/register.html', {'form': form})
