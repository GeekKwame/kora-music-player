"""
WSGI entry point bridge for cloud providers that default to `app:app` (such as Render).
"""
from music.wsgi import application as app
