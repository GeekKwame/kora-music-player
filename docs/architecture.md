# Architecture

## System Overview

Kora is a server-rendered Django application with an embedded client-side HTML5 audio engine. The application serves dynamic discovery pages, handles user accounts and avatar media, queries the Spotify23 API via RapidAPI for catalogue data, and streams localized African soundscapes with global player controls.

```text
Browser (Client)
  |
  +-- [HTTPS] ---> Django / Gunicorn (Render / Web Server)
  |                  |
  |                  +---> PostgreSQL (or SQLite Fallback)
  |                  |       |-- Users, Sessions, Auth
  |                  |       +-- Profiles & Avatar metadata
  |                  |
  |                  +---> RapidAPI Spotify23 (Search & Artist metadata)
  |                  |
  |                  +---> WhiteNoise (Versioned static CSS, JS, Audio WAV files)
  |                  |
  |                  +---> Media Engine (User-uploaded profile pictures)
  |
  +-- [HTML5 Audio API] ---> Persistent Global Audio Dock (base.html)
                               |
                               +<---> Standalone Player Interface (music.html)
```

## Core Components

| Component | Path | Responsibility |
| --- | --- | --- |
| **Settings & URLs** | `music/` | Django configuration, URL routing, WSGI/ASGI entrypoints, security headers, WhiteNoise storage. |
| **Data Models** | `music_app/models.py` | `Profile` model (1:1 with `User`), file-based avatars (`avatar`), presets (`avatar_url`), auto-creation signals. |
| **View Controllers** | `music_app/views.py` | Page rendering, auth (`signup`, `login`, `logout`), avatar updates, standalone player (`music_player`), health check (`health_check`). |
| **Spotify Service** | `music_app/spotify_service.py` | RapidAPI client, error handling, in-memory caching (1h TTL), soundscape audio resolution (`get_soundscape_audio`). |
| **Audio Engine** | `templates/base.html` | Embedded `<audio id="global-audio">`, event bus, seeking scrubber, volume slider, queue management, spacebar controls. |
| **Player Page** | `templates/music.html` | Full-screen now playing UI, rotating vinyl/cover art, repeat/shuffle toggles, bidirectional sync with `window.koraPlayer`. |
| **Soundscapes** | `static/audio/` | Five high-fidelity 16-bit 44.1kHz stereo audio files representing major African genres. |
| **Templates** | `templates/` | Semantic HTML5 templates styled with modern design tokens, responsive layouts, glassmorphic docks. |
| **Styles** | `static/style.css` | Modular vanilla CSS design system, CSS variables, dark-mode styling, responsive breakpoints. |

---

## Audio Soundscape Engine Architecture

Because Spotify deprecated 30-second preview URLs for third-party developer APIs in late 2024, Kora provides a high-fidelity native audio engine paired with handcrafted African soundscapes:

### 1. Soundscape Library
Five 16-bit 44.1kHz stereo WAV soundscapes are distributed via WhiteNoise:
- `african_lofi_experience.wav`: 85 BPM relaxed lofi kalimba chords and mellow Rhodes pianos.
- `afrobeat_essentials.wav`: 108 BPM polyrhythmic Afrobeat kicks, shekere, brass stabs, and guitar riffs.
- `amapiano_heat.wav`: 112 BPM South African Amapiano with log drum basslines and jazzy electric pianos.
- `highlife_classics.wav`: 115 BPM Palmwine highlife guitar arpeggios and conga rhythms.
- `desert_blues.wav`: 92 BPM Tuareg desert blues guitar slides and calabash pulses.

### 2. Audio URL Resolution
`spotify_service.get_soundscape_audio(key)` maps any track title or Spotify ID deterministically to one of the soundscape files using character hashing, ensuring every song discovered in the catalogue has immediate, working audio.

### 3. Client-Side Event Architecture
`base.html` creates `window.koraPlayer` and broadcasts custom DOM events on the document:
- `kora:playstate`: Emitted on play/pause, carrying `{ isPlaying, track }`.
- `kora:trackchange`: Emitted when a new track is queued or triggered.
- `kora:timeupdate`: Emitted as audio plays, carrying `{ currentTime, duration, ratio }`.

The standalone player (`templates/music.html`) listens to these events to update its timeline, rotating album disc animations, and playback controls in lockstep without audio restart.

---

## Data Models & Storage

### Profile Model (`music_app.models.Profile`)
- `user`: `OneToOneField(User, on_delete=models.CASCADE, related_name='profile')`.
- `avatar`: `FileField(upload_to='avatars/', blank=True, null=True)`.
- `avatar_url`: `CharField(max_length=500, blank=True, default='')` for preset avatar URLs.
- `get_avatar_url()`: Evaluates uploaded file URL first; falls back to `avatar_url` preset; defaults to `None`.
- `User.avatar_url`: Injected property on Django `User` model for clean template access (`{{ request.user.avatar_url }}`).
- Automatically provisioned on `User` creation via `post_save` signal.

### Media Files
- User-uploaded avatars are stored under `MEDIA_ROOT` (`media/avatars/`).
- In production, media paths are served securely via `music/urls.py` `re_path(r'^media/(?P<path>.*)$')`.

---

## HTTP Route Surface

| Route | HTTP Methods | View Handler | Purpose |
| --- | --- | --- | --- |
| `/` | GET | `views.home` | Home discovery: hero banners, trending tracks, soundscape triggers. |
| `/music/` | GET | `views.music_player` | Dedicated standalone music player view with synced controls. |
| `/search/?q=` | GET | `views.search` | Live search for artists and tracks with audio playback rows. |
| `/artist/<artist_id>/` | GET | `views.profile` | Artist profile: header imagery, bio, popular releases. |
| `/signup/` | GET, POST | `views.signup` | User registration with picture upload or avatar presets. |
| `/login/` | GET, POST | `views.login` | Authentication session start. |
| `/logout/` | GET | `views.logout` | Session termination. |
| `/profile/avatar/` | POST | `views.update_avatar` | Update profile picture / preset from any page. |
| `/health/` | GET | `views.health_check` | Liveness health probe returning `{"status": "healthy"}`. |
| `/admin/` | ALL | Django Admin | Administrative backend. |
