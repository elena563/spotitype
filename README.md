# SpotiType (work in progress...)

SpotiType is a web application that, given a Spotify playlist or a list of 5 songs, can tell you what kind of listener you are.

The frontend is made with ReactJS, the backend uses a machine learning model (Random Forest Classifier) trained on [Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset), labelled through a K-Means clustering.  
  
To obtain user's playlists or songs for testing the model, it uses Spotify API from [Spotify for Developers](https://developer.spotify.com/).
However, Spotify's function for audio features was recently deprecated, so the [ReccoBeats API](https://reccobeats.com/docs/apis/reccobeats-api) was used to extract values.

#### Technologies:

Frontend: ReactJS (Vite), libraries: Recharts, Lucide (for icons)  
Backend: Python, libraries: Flask, Scikit-Learn, Pandas, NumPy, requests