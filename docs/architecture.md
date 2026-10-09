# Architecture

## System overview

Kora is a server-rendered Django application. A browser requests a Django view, which renders a template using local static assets and, for discovery pages, normalized data returned by the Spotify23 API via RapidAPI. PostgreSQL stores Django-managed state such as accounts, sessions, and administration data.

```text
Browser
  | HTTPS
  v
Django / Gunicorn -----> PostgreSQL
  |
  +-----> RapidAPI Spotify23 (search and artist metadata)
  |
  +-----> WhiteNoise (versioned static assets)
```

## Components

| Location | Responsibility |
| --- | --- |
| `music/` | Django settings, root URL routing, WSGI and ASGI entry points. |
| `music_app/views.py` | Page handlers, account sign-up/sign-in/sign-out, and health check. |
| `music_app/spotify_service.py` | RapidAPI client, response normalization, duration formatting, and process-local caching. |
| `templates/` | Django templates for the home, search, profile, authentication, and player interfaces. |
| `static/` | CSS, brand assets, icons, and images. |
| `docker-compose.yml` | Local PostgreSQL service. |
| `render.yaml` / `build.sh` | Render deployment blueprint and release build steps. |
| `.github/workflows/ci.yml` | CI checks against PostgreSQL. |

## Request flows

### Discovery

- `GET /` searches RapidAPI for `Afrobeats` and renders featured artists and tracks.
- `GET /search/?q=<query>` searches RapidAPI when a non-empty query is supplied.
- `GET /artist/<artist_id>/` retrieves an artist overview and top tracks. If that lookup fails, the application attempts a search using the supplied value and then retries with the first artist ID.

The RapidAPI client applies a 10-second outbound timeout. Successful search and artist results are held in an in-process cache for one hour. The cache is not shared across Gunicorn workers and is cleared on a deployment or restart.

### Accounts

`/signup/`, `/login/`, and `/logout/` use Django’s built-in `User`, authentication, session, CSRF, and messages frameworks. There are no application-defined database models or migrations at present; `migrate` still creates Django’s built-in tables.

### Static assets

WhiteNoise serves the output of `collectstatic`. Production static files are content-hashed through `CompressedManifestStaticFilesStorage`.

## HTTP surface

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET | Home and featured discovery. |
| `/health/` | GET | Liveness response: `{"status":"healthy"}`. |
| `/search/?q=` | GET | Artist and track search. |
| `/artist/<artist_id>/` | GET | Artist profile and top tracks. |
| `/signup/` | GET, POST | Create a local user account. |
| `/login/` | GET, POST | Authenticate a local user. |
| `/logout/` | GET | End the current session. |
| `/admin/` | Django admin | Administrative interface (requires a staff user). |

The browser player updates display state only; it does not play full audio streams.

