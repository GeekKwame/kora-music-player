from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# Create your views here.
def home(request):
    return render(request, 'index.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')

        # Validations
        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif password != repeat_password:
            messages.error(request, 'Passwords do not match.')
        elif len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters long.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
        elif email and User.objects.filter(email=email).exists():
            messages.error(request, 'An account with this email already exists.')
        else:
            # Create user and log them in
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            auth_login(request, user)
            messages.success(request, f'Welcome to Kora, {username}!')
            return redirect('home')

    return render(request, 'signup.html')


def login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        if not username or not password:
            messages.error(request, 'Please enter both username and password.')
        else:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def logout(request):
    auth_logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')
