# SpotiType (work in progress...)

SpotiType is a web application that, given a Spotify playlist or a list of 5 songs, can tell you what kind of listener you are.

The frontend is made with ReactJS, the backend uses a machine learning model (Random Forest Classifier) trained on [Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset), labelled through a K-Means clustering.  
  
To obtain user's playlists or songs for testing the model, it uses Spotify API from [Spotify for Developers](https://developer.spotify.com/).
However, Spotify's function for audio features was recently deprecated, so the [ReccoBeats API](https://reccobeats.com/docs/apis/reccobeats-api) was used to extract values.


#### Project Structure
```
/root  
│  
├── frontend/  
│  ├── public/                  # assets  
│  ├── src/  
│  │  ├── components/  
│  │  │  ├── ResultChart.jsx    # spider plot for results  
│  │  │  ├── UploadForm.jsx  
│  │  │  └── Type.jsx           # profile component UI  
│  │  ├── App.jsx  
│  │  ├── main.jsx  
│  │  └── style.css  
│  └── index.html  
├── backend/  
│  ├── data/                    # raw, clean, scaled and clustered datasets  
│  ├── models/                  # scaler and randomforestclassifier pickle files  
│  ├── notebooks/  
│  │  ├── eda.ipynb             # exploratory analysis of variables  
│  │  └── ca.ipynb              # clusters analysis and interpretation  
│  ├── preprocess.py    
│  ├── clustering.py  
│  ├── main.py                  # run preprocess and clustering  
│  ├── train_model.py  
│  ├── spotify_utils.py         # API calls for Spotify and ReccoBeats  
│  └── app.py                   # Flask app  
└── README.md  
```


#### Technologies:

Frontend: ReactJS (Vite), libraries: Recharts, Lucide (for icons)  
Backend: Python, libraries: Flask, Scikit-Learn, Pandas, NumPy, requests