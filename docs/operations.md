# Operations and deployment

## Deployment target

`render.yaml` defines a Python web service. Its build command is `./build.sh`, which installs dependencies, collects static assets, and applies database migrations. The process command is `gunicorn music.wsgi:application`.

## Release procedure

1. Confirm CI passes: migration check, Django system checks, static collection, and tests.
2. Set the production variables described in [Configuration](configuration.md), especially `DATABASE_URL`, `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, and `RAPIDAPI_KEY`.
3. Deploy the commit through Render. Review build output: `collectstatic` and `migrate` must both succeed.
4. After the service becomes healthy, request `/health/` and load the home and search pages.
5. Monitor application logs for RapidAPI failures, database connection errors, template failures, and unexpected 5xx responses.

## Health checking

`GET /health/` returns HTTP 200 with `{"status":"healthy"}` and performs no database or RapidAPI work. Use it for process/load-balancer liveness. It does not prove that PostgreSQL or the external catalogue provider is available; include a separate synthetic search check if readiness coverage is required.

## Observability and known limits

- Application errors from RapidAPI are printed to standard output. Platform logs are the current error source.
- RapidAPI calls have a 10-second timeout and failures result in empty discovery data or an unavailable artist view rather than a 5xx response.
- The one-hour cache is in application memory, per worker. It is not a durable cache and does not provide a global quota guarantee across multiple instances.
- Database backups, uptime checks, alerts, request metrics, and error tracking are platform responsibilities and should be configured before a production launch.

## Rollback

For an application-only regression, redeploy the last known-good release in the hosting provider. If a release includes a database migration, review whether the migration is reversible before rolling back code. Take or confirm a managed database backup before schema-changing production deployments.

## Incident first checks

| Symptom | First checks |
| --- | --- |
| Service will not boot | Build logs, required environment variables, database URL, and migration output. |
| 400 host error | `ALLOWED_HOSTS` and the provider hostname. |
| Empty search or artist pages | `RAPIDAPI_KEY`, API quota/status, and outbound request errors in logs. |
| Static assets missing | Successful `collectstatic`, WhiteNoise configuration, and deployed build artifact. |
| Login or signup failures | Database reachability, migrations, session cookies, and Django auth logs. |

