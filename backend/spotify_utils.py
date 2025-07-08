import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv

load_dotenv()
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read"
))


def get_from_playlist(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    track_ids = []
    for item in tracks:
        track = item['track']
        if track:  # None check 
            track_ids.append(track['id'])

    return track_ids


def search_track(title):
    results = sp.search(q=title, limit=1, type='track')
    items = results.get('tracks', {}).get('items', [])
    if not items:
        return None
    return items[0]['id']


def get_features_dataframe(ids_list):
    url = "https://api.reccobeats.com/v1/track"
    params = {
        "ids": ids_list 
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print("Errore nella richiesta:", response.status_code)
        print(response.text)
        return None

    info = response.json()
    all_features = []

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
        features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness']
        df = df[features]
    else:
        print("Nessuna feature trovata")
        return None

    # data scaling
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    df_scaled = scaler.transform(df)

    return pd.DataFrame(df_scaled, columns=features)