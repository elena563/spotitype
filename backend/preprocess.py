import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

def preprocess_data(input_path, output_path, features_to_use):
    df = pd.read_csv(input_path)
    
    X = df[features_to_use]
    
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)

    with open('models/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)

    pd.DataFrame(X_scaled, columns=features_to_use).to_csv(output_path, index=False)

    return X_scaled
