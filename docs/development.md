# Development

## Local environment

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and set a valid `RAPIDAPI_KEY`.
4. Start PostgreSQL with `docker compose up -d`.
5. Run `python manage.py migrate` and `python manage.py runserver`.

The Compose database listens on port `5435` on the host and retains data in the named `postgres_data` volume. Stop it with `docker compose down`; this preserves the volume. Deleting the volume is destructive and is not part of normal teardown.

## Validation

Run the same basic validations as CI before opening a pull request:

```powershell
python manage.py makemigrations --check --dry-run
python manage.py check
python manage.py collectstatic --noinput
python manage.py test
```

The test suite uses Django’s test database and exercises public page rendering and the health endpoint. Views that call RapidAPI are written to fail gracefully, so tests do not require a live API key.

## Adding data models

There are currently no application models. When adding one:

```powershell
python manage.py makemigrations music_app
python manage.py migrate
python manage.py test
```

Commit generated migration files with the model change. The CI workflow rejects uncommitted migration changes.

## Code conventions

- Keep external API parsing and cache behavior in `music_app/spotify_service.py`.
- Keep request handling and presentation context in `music_app/views.py`.
- Use named URL patterns in templates rather than hard-coded local URLs.
- Add tests for each route, authentication branch, or normalized API response behavior you change.

