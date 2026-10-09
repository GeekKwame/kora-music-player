# Configuration

Kora is configured via environment variables. Copy `.env.example` to `.env` for local development. `.env` is ignored by Git and must never be committed to source control.

---

## Environment Variable Reference

| Variable | Required in Production | Default Value | Description |
| --- | --- | --- | --- |
| `SECRET_KEY` | **Yes** | Insecure development string | Cryptographic secret for session signing and CSRF tokens. Must be long and random in production. |
| `DEBUG` | **Yes** | `True` | Set to `False` in production. Controls detailed stack traces and production security checks. |
| `ALLOWED_HOSTS` | **Yes** | `localhost 127.0.0.1 [::1] testserver .onrender.com` | Space-separated list of allowed hostnames/domains. |
| `RENDER_EXTERNAL_HOSTNAME` | Managed by Render | Empty | Automatically appended to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` on Render. |
| `CSRF_TRUSTED_ORIGINS` | No | `https://*.onrender.com http://localhost:8000 http://127.0.0.1:8000` | Space-separated list of trusted origins for HTTPS POST requests. |
| `DATABASE_URL` | Recommended | Empty | Managed PostgreSQL connection string (`postgresql://user:pass@host:port/db`). Overrides all individual `DB_*` settings. |
| `DB_ENGINE` | No | `postgresql` | Set to `sqlite` to force SQLite storage locally or in lightweight containers. |
| `DB_NAME` | Local Compose only | `kora_db` | PostgreSQL database name. |
| `DB_USER` | Local Compose only | `kora_user` | PostgreSQL username. |
| `DB_PASSWORD` | Local Compose only | `kora_password123` | PostgreSQL password. |
| `DB_HOST` | Local Compose only | `localhost` | PostgreSQL host. |
| `DB_PORT` | Local Compose only | `5435` | PostgreSQL port (matches `docker-compose.yml`). |
| `RAPIDAPI_KEY` | Recommended | Empty | RapidAPI key for the Spotify23 catalogue API. Sent as `x-rapidapi-key`. |
| `RAPIDAPI_HOST` | No | `spotify23.p.rapidapi.com` | RapidAPI host for the Spotify23 API. |
| `SECURE_SSL_REDIRECT` | No | `True` (when `DEBUG=False`) | Enforces HTTPS redirection in production environments. |
| `SECURE_HSTS_SECONDS` | No | `31536000` (1 year) | HTTP Strict Transport Security duration applied when `DEBUG=False`. |
| `EMAIL_BACKEND` | No | `django.core.mail.backends.console.EmailBackend` in dev, `smtp.EmailBackend` in prod | Mailer backend for Django 6 `MAILERS` setting. |

---

## Database Precedence & Fallback Logic

Django configures the database connection in `music/settings.py` following this hierarchy:

1. **`DATABASE_URL`**: If set, parsed by `dj-database-url` with connection pooling (`conn_max_age=600`).
2. **Render Resilient Fallback**: If running on Render (`RENDER=true`) and no database host is configured, Kora defaults automatically to SQLite (`db.sqlite3`) to prevent `500 Internal Server Error` connection crashes.
3. **`DB_ENGINE=sqlite`**: Forces SQLite storage.
4. **Local PostgreSQL**: Connects to `DB_HOST:DB_PORT` using individual credentials matching Docker Compose.

---

## Production Setup Recommendations

1. **Secret Key**: Generate a 64-character random key:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```
2. **Render Environment Configuration**:
   - Set `DEBUG=False`.
   - Set `SECRET_KEY=<your-secret>`.
   - Set `RAPIDAPI_KEY=<your-rapidapi-key>`.
   - Set `DATABASE_URL` from your provisioned PostgreSQL instance.
