# Configuration

Copy `.env.example` to `.env` for local development. `.env` is ignored by Git and must never be deployed or committed. The settings module reads it from the repository root.

| Variable | Required | Default / behavior |
| --- | --- | --- |
| `SECRET_KEY` | Yes in production | Django has a development fallback; production must provide a unique, secret random value. |
| `DEBUG` | Yes in production | Defaults to `True`; set exactly `False`, `0`, or another false value for production. |
| `ALLOWED_HOSTS` | Yes in production | Space-separated hostnames. Defaults include local hosts and `.onrender.com`. |
| `DATABASE_URL` | Recommended in production | A PostgreSQL connection URL. When present, it overrides all `DB_*` variables. |
| `DB_NAME` | Local only | `kora_db`. |
| `DB_USER` | Local only | `kora_user`. |
| `DB_PASSWORD` | Local only | Local Compose default is `kora_password123`; replace it outside disposable local use. |
| `DB_HOST` | Local only | `localhost`. |
| `DB_PORT` | Local only | `5435`. |
| `RAPIDAPI_KEY` | Yes for catalogue data | RapidAPI credential sent as `x-rapidapi-key`. Without it, discovery requests fail gracefully and return empty results. |
| `RAPIDAPI_HOST` | No | `spotify23.p.rapidapi.com`; sent as `x-rapidapi-host` and used to build the API URL. |
| `RENDER_EXTERNAL_HOSTNAME` | Render-managed | Added to `ALLOWED_HOSTS` when supplied by Render. |

## Production values

- Generate and store `SECRET_KEY` in the hosting provider’s encrypted environment-variable store.
- Use a managed PostgreSQL `DATABASE_URL` with TLS as required by the provider.
- Set `DEBUG=False` and list only controlled domains in `ALLOWED_HOSTS`.
- Provision a RapidAPI subscription with capacity for application traffic. API keys are secrets and should be rotated immediately if exposed.

## Database precedence

When `DATABASE_URL` is configured, `dj-database-url` creates the Django connection with a 600-second connection lifetime. Otherwise Django connects using individual `DB_*` settings, matching the local Docker Compose service.

