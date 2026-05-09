import subprocess
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + '/..'))
from unittest.mock import patch
import pandas as pd
import numpy as np

from preprocess import preprocess_data
from clustering import run_clustering    

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + '/..')
input_file = os.path.join(BASE_DIR, 'tests', 'data', 'test_input.csv')
labelled_file = os.path.join(BASE_DIR, 'tests', 'data', 'test_input_labelled.csv')
train_model_path = os.path.join(BASE_DIR, 'train_model.py')
features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness', 'tempo']

def test_preprocess_data(tmp_path):
    output_file = tmp_path / "output_preprocess.csv"
    result = preprocess_data(input_file, str(output_file), features)
    assert isinstance(result, np.ndarray)
    assert output_file.exists()
    assert output_file.stat().st_size > 0

def test_run_clustering():
    result = run_clustering(input_file, n_clusters=3)
    assert isinstance(result, pd.DataFrame)
    model_path = os.path.join(BASE_DIR, 'models', 'cluster_model.pkl')
    data_path = os.path.join(BASE_DIR, 'data', 'clustered_data.csv')
    assert os.path.exists(model_path)
    assert os.path.exists(data_path)

def test_plot_clustering():
    with patch("matplotlib.pyplot.show") as mock_show:
        result = run_clustering(input_file, n_clusters=3, plot=True)
        assert isinstance(result, pd.DataFrame)
        mock_show.assert_called_once()

def test_train_model():
    train_model_path = os.path.join(BASE_DIR, 'train_model.py')
    result = subprocess.run([sys.executable, train_model_path, labelled_file])
    assert result.returncode == 0
    model_path = os.path.join(BASE_DIR, 'models', 'random_forest.pkl')
    assert os.path.exists(model_path)