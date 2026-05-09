import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/scaler.pkl')

def preprocess_data(input_path, output_path, features_to_use):
    try:
        df = pd.read_csv(input_path)
        X = df[features_to_use]
        
        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        with open(MODEL_PATH, 'wb') as f:
            pickle.dump(scaler, f)

        pd.DataFrame(X_scaled, columns=features_to_use).to_csv(output_path, index=False)
        print(type(X_scaled))
        return X_scaled
    except Exception as e:
        print(f"Preprocessing error: {e}")
        return None
