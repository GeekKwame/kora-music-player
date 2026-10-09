import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
RAPIDAPI_HOST = os.getenv("RAPIDAPI_HOST", "spotify23.p.rapidapi.com")

# In-memory cache to conserve RapidAPI quota: {cache_key: (timestamp, data)}
_CACHE = {}
CACHE_TTL = 3600  # 1 hour


def _get_headers():
    return {
        "x-rapidapi-key": os.getenv("RAPIDAPI_KEY", RAPIDAPI_KEY),
        "x-rapidapi-host": os.getenv("RAPIDAPI_HOST", RAPIDAPI_HOST),
    }


SOUNDSCAPE_TRACKS = [
    '/static/audio/african_lofi_experience.wav',
    '/static/audio/afrobeat_essentials.wav',
    '/static/audio/amapiano_heat.wav',
    '/static/audio/highlife_classics.wav',
    '/static/audio/desert_blues.wav',
]


def get_soundscape_audio(key):
    if not key:
        return SOUNDSCAPE_TRACKS[0]
    val = sum(ord(c) for c in str(key))
    return SOUNDSCAPE_TRACKS[val % len(SOUNDSCAPE_TRACKS)]


def format_duration(ms):
    if not ms:
        return "--:--"
    total_seconds = int(ms) // 1000
    minutes = total_seconds // 60
    seconds = total_seconds % 60
    return f"{minutes}:{seconds:02d}"


def search_spotify(query, limit=10):
    """
    Search Spotify for artists and tracks using RapidAPI Spotify23.
    Returns: {'artists': [...], 'tracks': [...]}
    """
    if not query or not query.strip():
        return {"artists": [], "tracks": []}

    query = query.strip()
    cache_key = f"search_{query.lower()}_{limit}"
    now = time.time()

    if cache_key in _CACHE:
        cached_time, cached_data = _CACHE[cache_key]
        if now - cached_time < CACHE_TTL:
            return cached_data

    url = f"https://{RAPIDAPI_HOST}/search/"
    params = {
        "q": query,
        "type": "multi",
        "offset": "0",
        "limit": str(limit),
        "numberOfTopResults": "5",
    }

    try:
        response = requests.get(url, headers=_get_headers(), params=params, timeout=10)
        if response.status_code != 200:
            print(f"[RapidAPI Error] Status {response.status_code}: {response.text[:200]}")
            return {"artists": [], "tracks": []}

        data = response.json()
        artists = []
        tracks = []

        # Parse artists
        raw_artists = (data.get("artists") or {}).get("items", [])
        for item in raw_artists:
            d = item.get("data") or {}
            profile = d.get("profile") or {}
            visuals = d.get("visuals") or {}
            avatar_image = visuals.get("avatarImage") or {}
            avatar_sources = avatar_image.get("sources", [])
            image_url = avatar_sources[0].get("url") if avatar_sources else "https://via.placeholder.com/300?text=Artist"
            uri = d.get("uri", "")
            artist_id = uri.split(":")[-1] if uri else ""

            if profile.get("name"):
                artists.append({
                    "id": artist_id,
                    "name": profile.get("name"),
                    "image_url": image_url,
                    "uri": uri,
                })

        # Parse tracks
        raw_tracks = (data.get("tracks") or {}).get("items", [])
        for item in raw_tracks:
            d = item.get("data") or {}
            album = d.get("albumOfTrack") or {}
            cover_art = album.get("coverArt") or {}
            cover_sources = cover_art.get("sources", [])
            image_url = cover_sources[0].get("url") if cover_sources else "https://via.placeholder.com/300?text=Track"

            track_artists = (d.get("artists") or {}).get("items", [])
            artist_names = ", ".join([
                (a.get("profile") or {}).get("name", "")
                for a in track_artists
                if (a.get("profile") or {}).get("name")
            ])
            first_artist_uri = track_artists[0].get("uri", "") if track_artists else ""
            artist_id = first_artist_uri.split(":")[-1] if first_artist_uri else ""

            duration_info = d.get("duration") or {}
            duration_ms = duration_info.get("totalMilliseconds", 0)

            if d.get("name"):
                tracks.append({
                    "id": d.get("id"),
                    "name": d.get("name"),
                    "artist_name": artist_names or "Unknown Artist",
                    "artist_id": artist_id,
                    "album_name": album.get("name", ""),
                    "image_url": image_url,
                    "duration": format_duration(duration_ms),
                    "audio_url": get_soundscape_audio(d.get("name") or d.get("id")),
                    "uri": d.get("uri", ""),
                })

        result = {"artists": artists, "tracks": tracks}
        _CACHE[cache_key] = (now, result)
        return result

    except Exception as e:
        print(f"[RapidAPI Exception] {e}")
        return {"artists": [], "tracks": []}


def get_artist_overview(artist_id):
    """
    Fetch artist profile, header visuals, stats, and top tracks.
    """
    if not artist_id:
        return None

    cache_key = f"artist_{artist_id}"
    now = time.time()

    if cache_key in _CACHE:
        cached_time, cached_data = _CACHE[cache_key]
        if now - cached_time < CACHE_TTL:
            return cached_data

    url = f"https://{RAPIDAPI_HOST}/artist_overview/"
    params = {"id": artist_id}

    try:
        response = requests.get(url, headers=_get_headers(), params=params, timeout=10)
        if response.status_code != 200:
            print(f"[RapidAPI Error] Status {response.status_code}: {response.text[:200]}")
            return None

        artist_data = (response.json().get("data") or {}).get("artist") or {}
        profile = artist_data.get("profile") or {}
        visuals = artist_data.get("visuals") or {}
        stats = artist_data.get("stats") or {}

        # Safely extract visuals
        header_image = visuals.get("headerImage") or {}
        avatar_image = visuals.get("avatarImage") or {}
        header_sources = header_image.get("sources", [])
        avatar_sources = avatar_image.get("sources", [])

        header_url = header_sources[0].get("url") if header_sources else (
            avatar_sources[0].get("url") if avatar_sources else "https://via.placeholder.com/800x400"
        )
        avatar_url = avatar_sources[0].get("url") if avatar_sources else header_url

        # Top tracks
        top_tracks = []
        discography = artist_data.get("discography") or {}
        top_tracks_data = discography.get("topTracks") or {}
        raw_top_tracks = top_tracks_data.get("items", [])

        for item in raw_top_tracks:
            track = item.get("track") or {}
            album = track.get("album") or {}
            cover_art = album.get("coverArt") or {}
            cover_sources = cover_art.get("sources", [])
            image_url = cover_sources[0].get("url") if cover_sources else avatar_url

            duration_info = track.get("duration") or {}
            duration_ms = duration_info.get("totalMilliseconds", 0)

            playcount = track.get("playcount", item.get("playcount", "0"))
            formatted_playcount = f"{int(playcount):,}" if str(playcount).isdigit() else str(playcount)

            top_tracks.append({
                "id": track.get("id"),
                "name": track.get("name"),
                "image_url": image_url,
                "duration": format_duration(duration_ms),
                "audio_url": get_soundscape_audio(track.get("name") or track.get("id")),
                "playcount": formatted_playcount,
            })

        biography_info = profile.get("biography") or {}
        monthly_listeners = stats.get("monthlyListeners", 0)

        result = {
            "id": artist_id,
            "name": profile.get("name", "Unknown Artist"),
            "biography": biography_info.get("text", ""),
            "header_url": header_url,
            "avatar_url": avatar_url,
            "monthly_listeners": f"{monthly_listeners:,}" if str(monthly_listeners).isdigit() else str(monthly_listeners),
            "top_tracks": top_tracks,
        }

        _CACHE[cache_key] = (now, result)
        return result

    except Exception as e:
        print(f"[RapidAPI Exception] {e}")
        return None
