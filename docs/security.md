# Security

## Current controls

- Django CSRF middleware protects the login and signup forms.
- Django’s built-in password validators and password hashing are enabled.
- Django’s authentication and session frameworks manage user sessions.
- WhiteNoise serves hashed production static files.
- `.env` and local virtual environments are ignored by Git.

## Production hardening checklist

Before handling real users or production traffic:

- Set `DEBUG=False` and replace the development fallback `SECRET_KEY` with a unique secret held only by the deployment platform.
- Restrict `ALLOWED_HOSTS` to owned domains; configure HTTPS/TLS at the edge.
- Configure secure-cookie and HTTPS redirect settings appropriate to the deployment topology (`CSRF_COOKIE_SECURE`, `SESSION_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`, and trusted proxy headers where applicable).
- Use a managed database with encrypted connections, backups, least-privilege credentials, and a rotation procedure.
- Store the RapidAPI key in a secret manager or encrypted platform variable; do not expose it to templates, client-side JavaScript, or logs.
- Establish error monitoring, access-log retention, alerting, dependency updates, and an incident response owner.
- Review the authentication design for the intended product: there is no email verification, password reset flow, rate limiting, or MFA today.

## External content

Artist artwork and metadata are sourced from an external provider, while several presentation images are loaded from Unsplash. Review provider terms, privacy obligations, availability expectations, and content/licensing requirements before production use.

