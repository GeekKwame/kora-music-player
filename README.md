# Kora Music Player

Kora is a Django web application for discovering African and global music. It provides server-rendered artist and track discovery, artist profiles, local account authentication, and a client-side player interface. Music catalogue data is obtained at request time from the Spotify23 API on RapidAPI; Kora does not stream audio or persist catalogue data.

## Contents

- [Architecture](docs/architecture.md)
- [Configuration](docs/configuration.md)
- [Development](docs/development.md)
- [Operations and deployment](docs/operations.md)
- [Security](docs/security.md)

## Quick start

Prerequisites: Python 3.10 or later, Docker Compose, and a RapidAPI key for the `spotify23` API.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
docker compose up -d
python manage.py migrate
python manage.py runserver
```

Set `RAPIDAPI_KEY` in `.env` before using search, artist profiles, or the featured content on the home page. Visit `http://127.0.0.1:8000/`; `http://127.0.0.1:8000/health/` returns a JSON liveness response.

## Common commands

```powershell
python manage.py check
python manage.py test
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
```

For deployment requirements, environment variables, release procedure, and rollback guidance, see [Operations](docs/operations.md). Never commit `.env` or production credentials.
