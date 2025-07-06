import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import pickle

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)


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


def get_features_dataframe(track_ids):
    features_list = sp.audio_features(tracks=track_ids)

    df = pd.DataFrame(features_list)

    features = ['danceability', 'energy', 'valence', 'acousticness',
                    'instrumentalness']

    df = df[features]

    # Scala i dati con il tuo scaler salvato
    with open('models/scaler.pkl', 'rb') as f:
        scaler = pickle.load(f)

    df_scaled = scaler.transform(df)

    return pd.DataFrame(df_scaled, columns=features)
