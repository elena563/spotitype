import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pickle
from sklearn.decomposition import PCA
import seaborn as sns

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/cluster_model.pkl')
NEW_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data/clustered_data.csv')

def run_clustering(data_path, n_clusters, plot=False):
    try:
        df = pd.read_csv(data_path)

        model = KMeans(n_clusters=n_clusters, random_state=42)
        labels = model.fit_predict(df)
        df['cluster'] = labels

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(model, f)

        # save clustering
        df.to_csv(NEW_DATA_PATH, index=False)

        if plot:
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(df)
            df_viz = pd.DataFrame(X_pca, columns=['PC1', 'PC2'])
            df_viz['cluster'] = labels

            sns.scatterplot(data=df_viz, x='PC1', y='PC2', hue='cluster', palette='Set2')
            plt.show() 

        return df

    except Exception as e:
        print(f"Clustering error: {e}")
        return None
