import { useState } from 'react';
import { CirclePlay, Music } from 'lucide-react';
import Loader from './Loader';
import Type from './Type';
import typeData from '../data/typeData';

function UploadForm() {
  const [activeTab, setActiveTab] = useState('playlist_form');
  const [playlistField, setPlaylistField] = useState("");
  const [songs, setSongs] = useState({
        song1: "",
        song2: "",
        song3: "",
        song4: "",
        song5: ""
      });
  const [result, setResult] = useState(null);
  const [features, setFeatures] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSongs(prev => ({ ...prev, [name]: value }));
    setError("");
  };

  const formatSong = (str) => {
    let s = str.trim();
    s = s.replace(/\s*-\s*/, " - ");
    return s;
  };


  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");

    // client side validation
    if (activeTab === "playlist_form"){
      if (playlistField.length === 0) {
        setError("Insert a playlist URL");
        return;
      } else if (!playlistField.startsWith("https://open.spotify.com/playlist/")) {   //TODO: edit this if add other sources
        setError("Inserisci un URL valido di una playlist Spotify.");
        return;
      }
    } else if (activeTab === "songs_form") {
      if (songs.song1.length === 0 || songs.song2.length === 0 || songs.song3.length === 0 || songs.song4.length === 0 || songs.song5.length === 0) {
        setError("Insert at least 5 songs");
        return;
      }
    }

    setLoading(true);
    let payload = { form_type: activeTab };

    if (activeTab === "playlist_form") {
      payload.playlistField = playlistField.trim();
    } else if (activeTab === "songs_form") {
      ["song1", "song2", "song3", "song4", "song5"].forEach((key) => {
        payload[key] = formatSong(songs[key]);
      });
    }

    fetch(import.meta.env.VITE_BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    })

    .then(async (res) => {
    const contentType = res.headers.get("content-type");

    let data;
    if (contentType && contentType.includes("application/json")) {
      data = await res.json();
    } else {
      const text = await res.text();
      throw new Error(text || "Errore generico");
    }

      if (!res.ok) {
        console.log("Errore backend:", data);
        setError(data.details || data.message || data.error || "Something went wrong.");
        setResult(null);
        setFeatures(null);
      } else {
        setResult(data.result);
        setFeatures(data.features);
        setError("");
      }
      setLoading(false);
    })
    .catch((err) => {
      console.error("Errore:", err);
      setError("Something went wrong.");
      setLoading(false);
    });
  };


  return (
    <div>
      <div style={{ width: 'min(1000px, 90%)' }} className="mx-auto mt-10 px-6 py-14 bg-[#917843] rounded-xl shadow gap-6 flex flex-col items-center">
        <h3 className="kanit-bold text-gray-100 text-4xl">Start now your music analysis</h3>
        <p className="font-semibold text-2xl text-gray-300">Choose how you want to share your musical tastes with us</p>
        <div className="flex gap-2 mb-4 p-2 bg-[#282b2e] w-[80%] rounded-lg">
          <button
            className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'playlist_form' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
            onClick={() => {setActiveTab('playlist_form'); setError("");}}
          >
            <CirclePlay /> Spotify Playlist 
          </button>
          <button
            className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'songs_form' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
            onClick={() => {setActiveTab('songs_form'); setError("");}}
          >
            <Music /> Favorite Songs
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 w-[80%] text-left">
          {activeTab === 'playlist_form' && (
            <div><p className="font-semibold text-2xl text-gray-100 mb-4">Spotify Playlist URL</p>
            <input type="hidden" name="form_type" value="playlist_form" />
            <input
              type="text"
              name="playlistField"
              placeholder="https://open.spotify.com/playlists/..."
              className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
              value={playlistField}
              onChange={(e) => setPlaylistField(e.target.value)} required
            /></div>
          )}

          {activeTab === 'songs_form' && (
            <div><p className="font-semibold text-2xl text-gray-100 mb-4">Your 5 favorite songs</p>
            <input type="hidden" name="form_type" value="songs_form" />
              {["song1", "song2", "song3", "song4", "song5"].map((songKey, idx) => (
                <div key={songKey}>
                  <p className="font-semibold text-lg text-gray-300 mb-2">Song {idx + 1}</p>
                  <input
                    type="text"
                    name={songKey}
                    placeholder="Artista - Titolo Canzone"
                    className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
                    value={songs[songKey]}
                    onChange={handleChange}
                    required
                  />
                </div>
              ))}
            </div>
          )}

          <button
            type="submit"
            className="w-full bg-[#1DB954] text-white py-2 rounded hover:bg-green-600"
            disabled={loading}
          >
            Submit
          </button>
        </form>
      </div>

      <div className='flex justify-center items-center my-10'>
        {loading && (
          <Loader />
        )}
      </div>

      <div>
          {error && (
            <div className='flex justify-center'>
              <p className="py-3 px-10 max-w-md font-bold bg-red-100 text-red-500 text-center rounded shadow border-2 border-red-500">
                {error}
              </p>
            </div>
          )}
          {result && features &&
          <div>
            <h3 className="text-center kanit-bold text-4xl mb-8 mt-16 text-white">Your Type is...</h3>
             <Type features={features} data={typeData[result]}/>
          </div>
          }
      </div>
    </div>
  );
}


export default UploadForm;
