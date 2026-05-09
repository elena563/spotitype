# SpotiType

SpotiType is a web application that, given a playlist or a list of 5 songs, can tell you what kind of listener you are.

The frontend is made with ReactJS, the backend uses a machine learning model (Random Forest Classifier) trained on [Kaggle Spotify Tracks Dataset](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset), labelled through a K-Means clustering.  
(Soon I will experiment and improve this ML part, stay tuned!)

Songs data are extracted through different open APIs. All the infrastructure was changed, since Spotify's API for songs search is not free anymore.
- [SpotifyScraper](https://spotifyscraper.readthedocs.io/en/latest/) package to get songs ids list from playlists. At the moment, only Spotify playlists are supported, but I will add support for other platforms in the future.
- [Deezer API](https://developers.deezer.com/api) to get songs data and extract their ISRC id
- [ReccoBeats API](https://reccobeats.com/docs/apis/reccobeats-api) was used to obtain audio feature values
Spotify functions will be maintained with old_ prefix, just in case Spotify's API becomes free again, so that the app can be easily switched back to it.


### App Usage
You can now use SpotiType UI [here](https://spotitype.vercel.app)!

If you want to try clustering and training the model on your own, you can clone the repo and run scripts locally.

### Technologies

#### Frontend:  
[![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)](https://reactjs.org/)  
[![Tailwind CSS](https://img.shields.io/badge/Tailwind%20CSS-06B6D4?style=flat&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)  
**Libraries:** Recharts, Lucide (for icons), styled-components (for Loader)

#### Backend:  
[![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)  
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)  
**Libraries:** Scikit-Learn, Pandas, NumPy, requests, Jupyter Notebook


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
│  ├── tests/                   # unit tests
│  │  ├── test_app.py
│  │  ├── test_music_utils.py
│  │  └── test_ml_functions.py
│  ├── preprocess.py    
│  ├── clustering.py  
│  ├── main.py                  # run preprocess and clustering  
│  ├── train_model.py  
│  ├── music_utils.py           # functions to get songs data from APIs
│  ├── spotify_utils.py         # old Spotify API functions, not used anymore  
│  └── app.py                   # Flask app  
└── README.md  
```


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