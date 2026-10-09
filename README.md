# Kora Music Player

A music player and streaming web application built with Django.

## Features
- Audio player interface with playlists and track browsing
- User authentication (login, signup, profile)
- Search and library navigation
- Responsive styling

## Project Structure
- `music/`: Django core project settings and routing
- `music_app/`: Main Django app handling views and models
- `templates/`: HTML templates for UI views
- `static/`: CSS styles, branding assets, and favicons

## Getting Started

### Prerequisites
- Python 3.10+
- Docker & Docker Compose (for local PostgreSQL)

### Local Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start local PostgreSQL via Docker:
   ```bash
   docker compose up -d
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Free Deployment (Render + Neon)
1. **Database:** Create a free serverless PostgreSQL database at [Neon.tech](https://neon.tech) and copy your connection string.
2. **Web Service:** Create a new Web Service on [Render.com](https://render.com) connected to this GitHub repo.
3. **Build & Start Commands:**
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn music.wsgi:application`
4. **Environment Variables on Render:**
   - `DATABASE_URL`: Your Neon Postgres connection string
   - `DEBUG`: `False`
   - `SECRET_KEY`: A secure random secret key
