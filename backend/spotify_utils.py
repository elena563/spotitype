import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from requests.adapters import HTTPAdapter
from spotipy.exceptions import SpotifyException
from requests.sessions import Session
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/scaler.pkl')

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

class TimeoutSession(requests.Session):
    def request(self, *args, **kwargs):
        kwargs.setdefault('timeout', 20)
        return super().request(*args, **kwargs)

session = TimeoutSession()
adapter = HTTPAdapter(max_retries=3)
session.mount('https://', adapter)
session.mount('http://', adapter)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
    )
)

sp2 = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))


def old_get_from_playlist(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
    except SpotifyException as e:
        print(f"Spotify error: {e}")
        return None
    tracks = results['items']

    track_ids = []
    for item in tracks:
        track = item['track']
        if track:  # None check, if none skip track 
            track_ids.append(track['id'])

    return track_ids


def old_search_track(title):
    try:
        results = sp2.search(q=title, limit=1, type='track')
        items = results.get('tracks', {}).get('items', [])
        if not items:
            return None
        return items[0]['id']
    except Exception as e:
        print(f"Spotify search error: {e}")
        return None