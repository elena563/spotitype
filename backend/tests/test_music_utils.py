import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))

import pandas as pd
from music_utils import search_track, get_from_playlist, get_features_dataframe, similarity, chunk_list
from unittest.mock import patch

def test_get_from_valid_playlist():
    playlist = 'https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC?si=9d6f9f1f6b4c4d1f'
    result = get_from_playlist(playlist)
    assert isinstance(result, list)
    assert len(result) > 0

def test_get_from_invalid_playlist():
    playlist = 'https://open.spotify.com/playlist/invalid'
    result = get_from_playlist(playlist)
    assert result is None

def test_similarity():
    assert similarity("test", "test") == 1.0
    assert similarity("test", "toast") < 1.0

def test_search_track_found():
    result = search_track("The Weeknd - Blinding Lights")
    assert result is not None
    assert "title" in result and "artist" in result

def test_search_track_not_found():
    result = search_track("asdkjhasdkjhaskjdhakjsdh")
    assert result is None

def test_chunk_list():
    data = [1,2,3,4,5]
    chunks = list(chunk_list(data, 2))
    assert chunks == [[1,2],[3,4],[5]]


@patch("music_utils.requests.get")
def test_get_features_dataframe_mocked(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.side_effect = [
        {"content": [{"id": "fakeid", "isrc": "fakeisrc"}]}, 
        {"danceability": 0.5, "energy": 0.5, "valence": 0.5, "acousticness": 0.5, "instrumentalness": 0.5, "liveness": 0.5, "speechiness": 0.5, "tempo": 120}  # seconda chiamata
    ]
    with patch("music_utils.pickle.load") as mock_scaler_load:
        class DummyScaler:
            def transform(self, df):
                return df.values
        mock_scaler_load.return_value = DummyScaler()
        result = get_features_dataframe(["fakeisrc"])
        assert result is not None
        assert isinstance(result, pd.DataFrame)
        assert "danceability" in result.columns