import os
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
import pickle
from marshmallow import ValidationError

from music_utils import search_track, get_from_playlist, get_features_dataframe
from schemas import PlaylistFormSchema, SongsFormSchema

# configure application
app = Flask(__name__)
CORS(app, origins=[
    "http://localhost:5173",
    "https://spotitype.vercel.app"
])
app.debug = True

# load machine learning model
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models/random_forest.pkl')
with open(MODEL_PATH, 'rb') as f:
    model = pickle.load(f)

# prevent caching
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

class APIError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

@app.errorhandler(APIError)
def handle_api_error(error):
    response_data = {
        "message": "Invalid input",
        "details": error.message
    }
    return jsonify(response_data), error.status_code

@app.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "GET":
            # frontend is set in react
            return "OK", 200
        
        data = request.get_json(silent=True)
        if not data:
            raise APIError("Missing data", 400)
        
        form_type = data.get('form_type')
        if form_type not in ['playlist_form', 'songs_form']:
            raise APIError("Invalid or missing form_type", 400)

        if form_type == 'playlist_form':
            try:
                validated = PlaylistFormSchema().load(data)
            except ValidationError as err:
                raise APIError(err.messages, 400)
            
            playlist_url = validated['playlistField']

            playlist_id = playlist_url.split("/")[-1].split("?")[0]

            tracks = get_from_playlist(playlist_url)
            if tracks is None or len(tracks) == 0:
                raise APIError("Playlist URL is invalid or playlist is empty", 400)

        elif form_type == 'songs_form':
            try:
                validated = SongsFormSchema().load(data)
            except ValidationError as err:
                raise APIError(f"Invalid input: {err.messages}", 400)
            
            songs = [validated['song1'], validated['song2'], validated['song3'], validated['song4'], validated['song5']]
            tracks = []
            for title in songs:
                track = search_track(title) 
                if track is not None and track['isrc'] is not None:
                    tracks.append(track['isrc'])
                else:
                    print(track)
                    print(title)
                    raise APIError("At least one song was not found", 400)
                
        X_test = get_features_dataframe(tracks)
        if X_test.empty:
            raise APIError("Error in getting features", 400)
        X_test1= X_test.drop(columns=['liveness', 'speechiness', 'tempo'])
        X_test_avg = X_test1.mean().to_frame().T
        y_pred = model.predict(X_test_avg)          # output will be 0, 1, 2, 3, 4 or 5

        features_dict = X_test_avg.iloc[0].to_dict()

        return jsonify({"result": y_pred[0].item(), "features": features_dict})
    
    except APIError:
        raise
    
    except Exception as e:
        print(f"Internal server error: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
#if __name__ == "__main__":
#    app.run(debug=True)
