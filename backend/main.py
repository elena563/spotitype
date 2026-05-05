from preprocess import preprocess_data
from clustering import run_clustering

features = ['danceability', 'energy', 'valence', 'acousticness', 'instrumentalness', 'liveness', 'speechiness', 'tempo']

result = preprocess_data('data/cleaned_data.csv', 'data/scaled_data.csv', features)
if result is None:
    print("Preprocessing failed. Aborting pipeline.")
    exit(1)

result = run_clustering('data/scaled_data.csv', n_clusters=6)
if result is None:
    print("Clustering failed. Aborting pipeline.")
    exit(1)
