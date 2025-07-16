from flask import Flask, render_template, request
from flask_cors import CORS
from flask import jsonify
import pickle
from spotify_utils import get_from_playlist, search_track, get_features_dataframe

# configure application
app = Flask(__name__)
CORS(app)
app.debug = True

# prevent caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET, POST"])
def index():
        if request.method == "GET":
            return "OK", 200
        data = request.get_json()
        form_type = data.get('form_type')
        with open('models/random_forest.pkl', 'rb') as f:
            model = pickle.load(f)


        if form_type == 'playlist_form':
            playlist_url = data.get('playlistField')

            playlist_id = playlist_url.split("/")[-1].split("?")[0]

            tracks = get_from_playlist(playlist_id)
            if tracks is None or len(tracks) == 0:
                 return jsonify({"error": "Playlist URL is invalid or playlist is empty"}), 400

        elif form_type == 'songs_form':
            songs = [data.get('song1'),
                    data.get('song2'),
                    data.get('song3'),
                    data.get('song4'),
                    data.get('song5')]
            tracks = []
            for title in songs:
                track = search_track(title) 
                if track:
                    tracks.append(track)
                else:
                    return jsonify({"error": "At least one song was not found"}), 400

            
        X_test = get_features_dataframe(tracks)
        X_test1= X_test.drop(columns=['liveness', 'speechiness', 'tempo'])
        X_test_avg = X_test1.mean().to_frame().T
        y_pred = model.predict(X_test_avg) # output will be 0, 1, 2, 3, 4 or 5

        features_dict = X_test_avg.iloc[0].to_dict()

        return jsonify({"result": y_pred[0].item(), "features": features_dict})
    
#if __name__ == "__main__":
#    app.run(debug=True)
