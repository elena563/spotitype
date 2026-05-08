import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b"OK"

def test_index_no_data(client):
    response = client.post('/', json={})
    assert response.status_code == 400
    assert b"Missing data" in response.data

def test_index_invalid_form_type(client):
    response = client.post('/', json={'form_type': 'invalid'})
    assert response.status_code == 400
    assert b"Invalid or missing form_type" in response.data

def test_index_invalid_playlist_url(client):
    response = client.post('/', json={'form_type': 'playlist_form', 'playlistField': 'invalid'})
    assert response.status_code == 400
    assert b"Playlist URL is invalid or playlist is empty" in response.data

def test_index_empty_playlist_url(client):
    response = client.post('/', json={'form_type': 'playlist_form', 'playlistField': ''})
    assert response.status_code == 400
    assert b"Invalid input" in response.data

def test_index_missing_songs(client):
    response = client.post('/', json={'form_type': 'songs_form'})
    assert response.status_code == 400
    assert b"Invalid input" in response.data

def test_index_invalid_type_song(client):
    response = client.post('/', json={
        'form_type': 'songs_form', 'song1': 5, 'song2': 'The Weeknd - Blinding Lights', 'song3': 'Tom Odell - Another Love', 'song4': 'Ed Sheeran - Shape of You', 'song5': 'Ariana Grande - positions'
        })
    assert response.status_code == 400
    assert b"Invalid input" in response.data

def test_index_empty_song(client):
    response = client.post('/', json={
        'form_type': 'songs_form', 'song1': '', 'song2': 'The Weeknd - Blinding Lights', 'song3': 'Tom Odell - Another Love', 'song4': 'Ed Sheeran - Shape of You', 'song5': 'Ariana Grande - positions'
        })
    assert response.status_code == 400
    assert b"Invalid input" in response.data

def test_index_song_not_found(client):
    response = client.post('/', json={
        'form_type': 'songs_form', 'song1': 'invalid-song', 'song2': 'The Weeknd - Blinding Lights', 'song3': 'Tom Odell - Another Love', 'song4': 'Ed Sheeran - Shape of You', 'song5': 'Ariana Grande - positions'
        })
    assert response.status_code == 400
    assert b"At least one song not found" in response.data

def test_index_valid_playlist(client):
    response = client.post('/', json={
        'form_type': 'playlist_form', 'playlistField': 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC?si=9d6f9f1f6b4c4d1f'
    })
    assert response.status_code == 200

def test_index_valid_songs(client):
    response = client.post('/', json={
        'form_type': 'songs_form', 'song1': 'The Weeknd - Blinding Lights', 'song2': 'The Weeknd - Blinding Lights', 'song3': 'Tom Odell - Another Love', 'song4': 'Ed Sheeran - Shape of You', 'song5': 'Ariana Grande - positions'
        })
    assert response.status_code == 200