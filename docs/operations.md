# Operations & Deployment

## Deployment Target (Render)

Kora is configured for native deployment on [Render](https://render.com) using the blueprint defined in [render.yaml](file:///c:/Users/eddie/OneDrive/Documents/projects/kora-music-player/render.yaml):
- **Build Command**: `./build.sh` (runs `pip install`, `collectstatic --no-input`, and `python manage.py migrate`).
- **Start Command**: `gunicorn music.wsgi:application`.
- **Environment**: Python 3.12, Gunicorn WSGI, WhiteNoise static files, PostgreSQL (or SQLite fallback).

---

## Release Procedure

1. **Local Pre-Flight**:
   ```powershell
   python manage.py makemigrations --check --dry-run
   python manage.py check
   python manage.py test
   ```
2. **Environment Configuration**:
   Ensure the following environment variables are set in the Render Dashboard:
   - `SECRET_KEY`: Long, random production secret.
   - `DEBUG`: `False`.
   - `DATABASE_URL`: Managed PostgreSQL connection string (or omit to utilize resilient SQLite fallback).
   - `RAPIDAPI_KEY`: Spotify23 RapidAPI subscription key.
3. **Trigger Deploy**:
   Push to the `main` branch on GitHub. Render will automatically execute `./build.sh` and deploy the updated container.
4. **Post-Deploy Verification**:
   - Check `/health/` returns `{"status": "healthy"}` (HTTP 200).
   - Verify home page [https://kora-music-player.onrender.com](https://kora-music-player.onrender.com) loads.
   - Test playback on the standalone player at `/music/`.

---

## Health Monitoring & Uptime Keep-Alive

Render's free tier spins down web services after 15 minutes of inactivity. To keep Kora continuously responsive and avoid cold starts:

1. Create a free account on [UptimeRobot](https://uptimerobot.com).
2. Configure a new **HTTP(s) Monitor**:
   - **URL**: `https://<your-service>.onrender.com/health/` *(Important: Point directly to `/health/` rather than `/` to avoid hitting database or third-party APIs during liveness checks)*.
   - **Monitoring Interval**: 5 minutes.
   - **Alert Threshold**: 2 failed attempts.
3. `/health/` executes a lightweight in-memory JSON response (`{"status": "healthy"}`) with zero external dependencies, guaranteeing instant 200 OK responses to pingers.

---

## Incident Troubleshooting Guide

| Symptom | Root Cause | Resolution |
| --- | --- | --- |
| **HTTP 500 on root (`/`)** | Database connection failure or unhandled exception during cold start. | Verify `DATABASE_URL` is accessible. Kora automatically falls back to SQLite on Render if `DATABASE_URL` is omitted. Check Render runtime logs. |
| **HTTP 403 Forbidden on login/signup** | Missing `CSRF_TRUSTED_ORIGINS` when submitting forms over HTTPS. | Ensure `CSRF_TRUSTED_ORIGINS` includes `https://*.onrender.com` (configured by default in `music/settings.py`). |
| **Infinite 301 Redirect Loop** | Render terminates SSL at edge proxy, but Django is unaware without proxy header. | Ensure `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` is present in `settings.py` (configured by default). |
| **Empty Search or Artist Profiles** | `RAPIDAPI_KEY` invalid, missing, or rate-limited (`429`). | The app gracefully falls back to curated African playlists and soundscapes. Check RapidAPI quota in the RapidAPI developer dashboard. |
| **Static files or soundscapes 404** | `collectstatic` failed during deployment build. | Check `./build.sh` logs in Render. WhiteNoise serves collected assets with content hashing from `STATIC_ROOT`. |
