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

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read"
    ),
    requests_session=session
)

sp2 = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
))


def get_from_playlist(playlist_id):
    try:
        results = sp.playlist_tracks(playlist_id)
    except SpotifyException:
        return None
    tracks = results['items']

    track_ids = []
    for item in tracks:
        track = item['track']
        if track:  # None check 
            track_ids.append(track['id'])

    return track_ids


def search_track(title):
    results = sp2.search(q=title, limit=1, type='track')
    items = results.get('tracks', {}).get('items', [])
    if not items:
        return None
    return items[0]['id']

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_features_dataframe(ids_list):
    all_features = []

    for chunk in chunk_list(ids_list, 40):
        url = "https://api.reccobeats.com/v1/track"
        params = {
            "ids": chunk 
        }

        try:
            response = requests.get(url, params=params, timeout=15)
            response.raise_for_status()
        except requests.exceptions.Timeout:
            print("Timeout nella richiesta iniziale a Reccobeats.")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Errore nella richiesta: {e}")
            return None

        info = response.json()
    

        for traccia in info['content']:
            rb_id = traccia['id']
            url_feat = f'https://api.reccobeats.com/v1/track/{rb_id}/audio-features'
            headers = { 'Accept': 'application/json' }
            r = requests.get(url_feat, headers=headers)
            if r.status_code == 200:
                feat = r.json()
                all_features.append(feat)
            else:
                print(f"Errore per traccia {rb_id}: {r.status_code}")

    if all_features:
        df = pd.DataFrame(all_features)
        features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness', 'tempo']

        for col in features:
            if col not in df.columns:
                df[col] = 0
        df = df[features]
    else:
        print("Nessuna feature trovata")
        return None

    # data scaling
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    df_scaled = scaler.transform(df)

    return pd.DataFrame(df_scaled, columns=features)