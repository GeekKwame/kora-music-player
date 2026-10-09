
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .spotify_service import search_spotify, get_artist_overview

# Create your views here.
def health_check(request):
    return JsonResponse({"status": "healthy"})


def home(request):
    # Fetch featured music and artists (cached)
    spotify_data = search_spotify('Afrobeats', limit=8)
    context = {
        'featured_artists': spotify_data.get('artists', []),
        'featured_tracks': spotify_data.get('tracks', []),
    }
    return render(request, 'index.html', context)


def search(request):
    query = request.GET.get('q', '').strip()
    artists = []
    tracks = []

    if query:
        results = search_spotify(query, limit=15)
        artists = results.get('artists', [])
        tracks = results.get('tracks', [])

    context = {
        'query': query,
        'artists': artists,
        'tracks': tracks,
    }
    return render(request, 'search.html', context)


def profile(request, artist_id):
    artist = get_artist_overview(artist_id)
    if not artist:
        # Fallback to general search if direct overview fails
        search_res = search_spotify(artist_id, limit=1)
        if search_res.get('artists'):
            artist = get_artist_overview(search_res['artists'][0]['id'])

    context = {
        'artist': artist,
    }
    return render(request, 'profile.html', context)


def music_player(request):
    return render(request, 'music.html')


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
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Handle profile picture option (file upload or chosen preset)
            avatar_file = request.FILES.get('avatar')
            avatar_preset = request.POST.get('avatar_preset', '').strip()

            from .models import Profile
            profile, _ = Profile.objects.get_or_create(user=user)
            if avatar_file:
                profile.avatar = avatar_file
                profile.avatar_url = ''
                profile.save()
            elif avatar_preset:
                profile.avatar_url = avatar_preset
                profile.save()

            user.refresh_from_db()
            auth_login(request, user)
            messages.success(request, f'Welcome to Kora, {username}!')
            return redirect('home')

    return render(request, 'signup.html')


def update_avatar(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        avatar_preset = request.POST.get('avatar_preset', '').strip()

        from .models import Profile
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if avatar_file:
            profile.avatar = avatar_file
            profile.avatar_url = ''
            profile.save()
            messages.success(request, 'Profile picture updated!')
        elif avatar_preset:
            profile.avatar_url = avatar_preset
            profile.avatar = None
            profile.save()
            messages.success(request, 'Profile picture updated!')

    return redirect(request.META.get('HTTP_REFERER', 'home'))


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
