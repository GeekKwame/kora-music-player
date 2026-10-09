# Development Guide

## Local Environment Setup

### 1. Python Environment
Ensure Python 3.10+ is installed. Create and activate a dedicated virtual environment:

```powershell
# Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Dependencies
Install all required packages:

```bash
pip install -r requirements.txt
```

### 3. Environment Variables
Copy `.env.example` to `.env`:

```powershell
Copy-Item .env.example .env
```
Provide your `RAPIDAPI_KEY` in `.env` to enable live Spotify searches.

### 4. Database Setup
Start local PostgreSQL via Docker Compose:

```bash
docker compose up -d
```
The database listens on host port `5435` and persists data in the `postgres_data` volume. Alternatively, set `DB_ENGINE=sqlite` in `.env` to run with zero external dependencies.

### 5. Run Migrations & Development Server
```bash
python manage.py migrate
python manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access the application.

---

## Validation & Quality Checks

Run the following validation sequence before opening pull requests or deploying:

```powershell
# 1. Ensure no model changes are missing migrations
python manage.py makemigrations --check --dry-run

# 2. Verify Django system configurations
python manage.py check

# 3. Verify production deployment security and settings
$env:DEBUG="False"; $env:SECRET_KEY="temporary-check-secret-with-more-than-50-characters-12345"; python manage.py check --deploy

# 4. Verify static assets collection and WhiteNoise manifest
python manage.py collectstatic --noinput

# 5. Run automated test suite
python manage.py test
```

---

## Database Migrations & Data Models

Kora defines models in `music_app/models.py` (such as `Profile` for user avatars). When adding or modifying models:

```powershell
python manage.py makemigrations music_app
python manage.py migrate
python manage.py test
```

Always commit newly generated migration files under `music_app/migrations/` alongside your model edits.

---

## Working with Soundscapes & Audio Assets

Audio assets reside in `static/audio/` and are distributed via WhiteNoise:
- Format: 16-bit 44.1kHz stereo WAV for universal browser playback without third-party audio preview dependencies.
- Audio URL mapping logic lives in `music_app/spotify_service.py` (`get_soundscape_audio`).
- Frontend audio player triggers live in `templates/base.html` (`window.koraPlayer`) and sync with `templates/music.html`.
