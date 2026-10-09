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
- `frontend/`: CSS styles and static assets

## Getting Started

### Prerequisites
- Python 3.10+
- virtualenv / venv

### Setup
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

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Start the development server:
   ```bash
   python manage.py runserver
   ```
   Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.
