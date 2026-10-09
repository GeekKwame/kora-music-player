# Security Policy & Hardening

## Security Controls Overview

Kora implements multi-layer security protections across HTTP transport, user sessions, form submissions, and media uploads:

### 1. Transport Security & Headers
When `DEBUG=False`:
- **SSL Redirection**: `SECURE_SSL_REDIRECT = True` redirects all plain HTTP requests to HTTPS.
- **Proxy SSL Header**: `SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')` informs Django of secure requests behind Render or reverse proxies.
- **HSTS (HTTP Strict Transport Security)**: `SECURE_HSTS_SECONDS = 31536000` with subdomains and preload flags enabled.
- **Clickjacking & MIME Protection**: `XFrameOptionsMiddleware` and `SECURE_CONTENT_TYPE_NOSNIFF` protect against UI redressing and MIME-confusion attacks.

### 2. Authentication & Session Protection
- **Secure Cookies**: `SESSION_COOKIE_SECURE = True` and `CSRF_COOKIE_SECURE = True` ensure session and CSRF tokens are only transmitted over TLS/HTTPS connections.
- **Password Policies**: Enforced through Django's `MinimumLengthValidator`, `CommonPasswordValidator`, `NumericPasswordValidator`, and `UserAttributeSimilarityValidator`.
- **CSRF Defense**: All POST endpoints (`/signup/`, `/login/`, `/profile/avatar/`) require Django `{% csrf_token %}` tokens. Trusted origins are validated against `CSRF_TRUSTED_ORIGINS`.

### 3. File Upload & Media Protection
- Avatar uploads are isolated in `media/avatars/`.
- Django validates uploaded file streams before disk storage.
- File paths are sanitized by Django's storage backend to prevent directory traversal (`../`).

### 4. API Credential Isolation
- RapidAPI credentials (`RAPIDAPI_KEY`) are read strictly from server-side environment variables via `music_app/spotify_service.py`.
- No third-party API tokens are ever passed into template contexts, browser cookies, or client-side JavaScript.

---

## Production Security Pre-Flight

Before launching into production, execute:

```powershell
$env:DEBUG="False"; $env:SECRET_KEY="<production-random-secret>"; python manage.py check --deploy
```

Verify that 0 errors and 0 warnings are emitted.
