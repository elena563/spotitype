from preprocess import preprocess_data
from clustering import run_clustering

features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness', 'tempo']

preprocess_data('data/cleaned_data.csv', 'data/scaled_data.csv', features)
run_clustering('data/scaled_data.csv', n_clusters=6)
