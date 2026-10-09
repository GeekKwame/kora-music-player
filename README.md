# Kora Music Player

[![Django CI](https://github.com/GeekKwame/kora-music-player/actions/workflows/ci.yml/badge.svg)](https://github.com/GeekKwame/kora-music-player/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-amber.svg)](LICENSE)
[![Python: 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Django: 5.x/6.x](https://img.shields.io/badge/Django-5.x%2F6.x-green.svg)](https://www.djangoproject.com/)

**Kora** is a production-grade Django web application dedicated to discovering and streaming African and global soundscapes. It combines server-rendered music exploration, live Spotify catalogue integration, authentic high-fidelity soundscapes, user profile customization with avatars, and a persistent client-side audio player dock.

Live Demo: [https://kora-music-player.onrender.com](https://kora-music-player.onrender.com)

---

## Key Features

- **African Soundscape Audio Engine**: Real HTML5 audio streaming with 5 handcrafted 16-bit 44.1kHz stereo soundscapes (*Afrobeat Essentials*, *Amapiano Heat*, *African Lofi Chill*, *Highlife Classics*, and *Desert Blues*).
- **Persistent Global Audio Dock**: Unified playback across all pages with real-time seeking, volume adjustment, mute toggling, queue skipping, and spacebar play/pause shortcuts.
- **Dedicated Player View (`/music/`)**: Full-screen player interface with animated album art, live scrubber, shuffle, loop repeat, and bidirectional synchronization with the global player dock.
- **Live Catalogue Search & Artist Profiles**: Spotify23 API integration on RapidAPI for searching tracks, artists, and exploring artist profiles with curated fallbacks.
- **User Authentication & Profile Avatars**: Local account management (`/signup/`, `/login/`, `/logout/`) with custom picture uploads or curated African aesthetic presets, populated seamlessly upon signing in.
- **Production-Ready & Resilient**:
  - Zero-downtime deployment on Render via `render.yaml` and `build.sh`.
  - Automatic HTTPS / reverse-proxy header support (`SECURE_PROXY_SSL_HEADER`, `CSRF_TRUSTED_ORIGINS`).
  - Resilient database handling: supports PostgreSQL with automatic fallback to SQLite.
  - Zero-dependency static asset delivery via WhiteNoise manifest compression.
  - Health check liveness probe at `/health/` for UptimeRobot monitoring.

---

## Project Documentation

Detailed guides and specifications are available in the [`docs/`](docs/) directory:

- [**Architecture**](docs/architecture.md) — Technical overview, request lifecycles, audio engine architecture, and HTTP surface.
- [**Configuration**](docs/configuration.md) — Environment variables, database connection strings, security toggles, and API keys.
- [**Development**](docs/development.md) — Local setup, Docker Compose PostgreSQL, running tests, and code style.
- [**Operations & Deployment**](docs/operations.md) — Render deployment blueprint, health checks, monitoring, and runbook.
- [**Security**](docs/security.md) — CSRF protection, secure cookies, upload validation, and production hardening checklist.

---

## Quick Start

### Prerequisites
- Python 3.10 or higher
- Git
- Docker Compose (optional, for local PostgreSQL)
- RapidAPI key for the `spotify23` API (optional; curated soundscapes run without API key)

### Local Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/GeekKwame/kora-music-player.git
   cd kora-music-player
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows PowerShell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # macOS / Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env

   # macOS / Linux
   cp .env.example .env
   ```
   *Edit `.env` to supply your `RAPIDAPI_KEY` and database credentials if desired.*

5. **Start PostgreSQL (Optional)**:
   ```bash
   docker compose up -d
   ```
   *Note: If PostgreSQL is not running, Kora can fall back to SQLite when `DB_ENGINE=sqlite` is configured.*

6. **Apply migrations and launch the server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

7. **Access the application**:
   - Web App: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - Standalone Player: [http://127.0.0.1:8000/music/](http://127.0.0.1:8000/music/)
   - Health Probe: [http://127.0.0.1:8000/health/](http://127.0.0.1:8000/health/)

---

## Quality & Production Verification

Run the full verification suite before pushing or deploying:

```powershell
# 1. Check for uncommitted migrations
python manage.py makemigrations --check --dry-run

# 2. Django system integrity check
python manage.py check

# 3. Production deployment hardening check
python manage.py check --deploy

# 4. WhiteNoise static assets collection
python manage.py collectstatic --noinput

# 5. Automated test suite
python manage.py test
```

---

## Deployment on Render

Kora includes native Render deployment configuration via [render.yaml](render.yaml) and [build.sh](build.sh):

1. Link your GitHub repository in the **Render Dashboard**.
2. Create a new **Web Service** using the repo Blueprint (`render.yaml`).
3. Set the following environment variables in Render:
   - `RAPIDAPI_KEY`: Your RapidAPI Spotify23 API key.
   - `DATABASE_URL`: Managed PostgreSQL connection string (or leave blank to use the resilient fallback).
4. Monitor the build output: `pip install`, `collectstatic`, and `migrate` will run automatically.
5. Set up an uptime monitor (such as [UptimeRobot](https://uptimerobot.com)) pointing to `https://<your-service>.onrender.com/health/` with a 5-minute interval to keep the free service responsive.
