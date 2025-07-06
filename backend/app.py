from flask import Flask, render_template, request
import pickle
from spotify_utils import get_from_playlist, search_track, get_features_dataframe

# configure application
app = Flask(__name__)
app.debug = True

# prevent caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        with open('models/random_forest.pkl', 'rb') as f:
            model = pickle.load(f)



        if form_type == 'playlist_form':
            playlist_url = request.form.get('playlistField')

            playlist_id = playlist_url.split("/")[-1].split("?")[0]

            tracks = get_from_playlist(playlist_id)
            if not tracks:
                return render_template("index.html", error='Playlist URL is invalid or playlist is empty')

        elif form_type == 'playlist_form':
            songs = [request.form.get('song1'),
                    request.form.get('song2'),
                    request.form.get('song3'),
                    request.form.get('song4'),
                    request.form.get('song5')]

            tracks = []
            for title in songs:
                track = search_track(title) 
                if track:
                    tracks.append(track)
                else:
                    return render_template("index.html", error='At least one song was not found')

            
        X_test = get_features_dataframe(tracks)
        y_pred = model.predict(X_test) # output will be 0, 1, 2, 3, 4 or 5

        return render_template("index.html", result=y_pred)

    else:
        return render_template("index.html")
    