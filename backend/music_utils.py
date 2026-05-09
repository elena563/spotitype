from spotify_scraper import SpotifyClient
import requests
import os
from requests.adapters import HTTPAdapter
import pandas as pd
import pickle
import requests
from dotenv import load_dotenv
from difflib import SequenceMatcher

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

RECCO_BASE = "https://api.reccobeats.com/v1"


def get_from_playlist(playlist_url: str):

    client = SpotifyClient()

    try:
        playlist = client.get_playlist_info(playlist_url)
    except Exception as e:
        print(f"[get_from_playlist] Spotify scraper error: {e}")
        client.close()
        return None
    finally:
        client.close()

    tracks = playlist.get("tracks", [])
    extracted_tracks = []

    for track in tracks:
        uri = track.get("uri", "")
        if not uri or "track:" not in uri:
            continue

        spotify_track_id = uri.split(":")[-1]
        extracted_tracks.append(spotify_track_id)

    return extracted_tracks

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def search_track(query: str):
    artist = ""
    title = query.strip()

    if " - " in query:
        artist, title = query.split(" - ", 1)

    artist = artist.strip()
    title = title.strip()

    if artist:
        deezer_query = f'artist:"{artist}" track:"{title}"'
    else:
        deezer_query = title

    try:
        response = requests.get(
            "https://api.deezer.com/search/track",
            params={
                "q": deezer_query,
                "limit": 5
            },
            timeout=10
        )
        response.raise_for_status()

    except requests.exceptions.Timeout:
        print("[search_track] Timeout Deezer")
        return None
    except requests.exceptions.RequestException as e:
        print(f"[search_track] Deezer request error: {e}")
        return None

    results = response.json().get("data", [])

    if not results:
        # fallback
        try:
            fallback = requests.get(
                "https://api.deezer.com/search/track",
                params={
                    "q": query,
                    "limit": 5
                },
                timeout=10
            )
            fallback.raise_for_status()
            results = fallback.json().get("data", [])

        except Exception as e:
            print(f"[search_track] Fallback error: {e}")
            return None

        if not results:
            print("[search_track] No result from fallback")
            return None

    # calculate similarity not to get random results for invalid queries
    best = None
    best_score = 0

    for track in results:
        candidate = f"{track.get('artist', {}).get('name', '')} - {track.get('title', '')}"
        score = similarity(query, candidate)

        if score > best_score:
            best_score = score
            best = track

    if best_score < 0.55:
        print("[search_track] No similar match found")
        return None

    deezer_id = best.get("id")
    deezer_title = best.get("title")
    deezer_link = best.get("link")
    preview = best.get("preview")
    duration = best.get("duration")
    rank = best.get("rank")
    isrc = best.get("isrc")

    artist_data = best.get("artist", {})
    deezer_artist = artist_data.get("name")
    artist_id = artist_data.get("id")
    album_data = best.get("album", {})
    album_title = album_data.get("title")
    cover = album_data.get("cover_medium")

    normalized_song = {
        "title": deezer_title,
        "artist": deezer_artist,
        "album": album_title,
        "duration": duration,
        "isrc": isrc,
        "preview": preview,
        "cover": cover,
        "rank": rank,

        "sources": {
            "deezer": {
                "track_id": deezer_id,
                "artist_id": artist_id,
                "link": deezer_link
            }
        }
    }
    return normalized_song


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
            print("Timeout in request to ReccoBeats.")
            return None

        except requests.exceptions.RequestException as e:
            print(f"Error in request: {e}")
            return None

        info = response.json()
        unique = {}

        for t in info["content"]:
            isrc = t.get("isrc")
            if isrc:
                unique[isrc] = t

        clean_tracks = list(unique.values())

        for track in clean_tracks:
            rb_id = track['id']
            url_feat = f'https://api.reccobeats.com/v1/track/{rb_id}/audio-features'
            headers = { 'Accept': 'application/json' }
            r = requests.get(url_feat, headers=headers)
            if r.status_code == 200:
                feat = r.json()
                all_features.append(feat)
            else:
                print(f"Error for track {rb_id}: {r.status_code}")

    if all_features:
        df = pd.DataFrame(all_features)
        features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness', 'tempo']

        for col in features:
            if col not in df.columns:
                df[col] = 0
        df = df[features]
    else:
        print("No features found")
        return None
    
    # data scaling
    try:
        with open(MODEL_PATH, 'rb') as f:
            scaler = pickle.load(f)
    except Exception as e:
        print(f"Scaler loading error: {e}")
        return None

    df_scaled = scaler.transform(df)

    return pd.DataFrame(df_scaled, columns=features)






# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":
    '''
    print("=" * 60)
    print("TEST search_track")
    print("=" * 60)

    test_queries = [
        "Cigarettes After Sex - Apocalypse",
        "The Weeknd - Blinding Lights",
        "Tom Odell - Another Love"
    ]

    for q in test_queries:

        result = search_track(q)

        if result:
            print("\nRISULTATO OK")
            print(result["title"])
            print(result["artist"])
            print(result["sources"]["deezer"]["track_id"])
        else:
            print("\nRisultato: None")'''
    print("\n")
    print("=" * 60)
    print("TEST get_from_playlist")
    print("=" * 60)

    playlist_id = "37i9dQZF1DXdPec7aLTmlC"

    tracks = get_from_playlist(playlist_id)

    if tracks:

        print("\nPrime 5 tracce:\n")

        for t in tracks[:5]:
            print(t)

    else:
        print("Fallito")