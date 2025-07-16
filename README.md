# SpotiType

SpotiType is a web application that, given a Spotify playlist or a list of 5 songs, can tell you what kind of listener you are.

The frontend is made with ReactJS, the backend uses a machine learning model (Random Forest Classifier) trained on [Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset), labelled through a K-Means clustering.  
  
To obtain user's playlists or songs for testing the model, it uses Spotify API from [Spotify for Developers](https://developer.spotify.com/).
However, Spotify's function for audio features was recently deprecated, so the [ReccoBeats API](https://reccobeats.com/docs/apis/reccobeats-api) was used to extract values.


### App Usage
You can now use SpotiType [here](https://spotitype.vercel.app)!


### Project Structure
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


### Technologies

#### Frontend:  
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)  
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)  
**Libraries:** Recharts, Lucide (for icons), styled-components (for Loader)

#### Backend:  
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)  
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)  
**Libraries:** Scikit-Learn, Pandas, NumPy, requests, Jupyter Notebook



### Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Contact

Elena Zen - [My Portfolio Website](https://elenazen.it) - info.elenazen@gmail.com