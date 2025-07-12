import { useState } from 'react';
import { Music } from 'lucide-react';
import { CirclePlay } from 'lucide-react';
import Type0 from './result/Type0';

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
  const [error, setError] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSongs(prev => ({ ...prev, [name]: value }));
  };


  const handleSubmit = (e) => {
  e.preventDefault();

  let payload = { form_type: activeTab };

  if (activeTab === "playlist_form") {
    payload.playlistField = playlistField;
  } else if (activeTab === "songs_form") {
    payload.songs = Object.values(songs);
  }

  fetch("http://localhost:5000/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })
    .then((res) => res.json())
    .then((data) => {
      if (data.error) {
        setError(data.error);
        setResult(null);
      } else {
        setResult(data.result);
        setError("");
      }
    })
    .catch((err) => {
      console.error("Errore:", err);
      setError("Something went wrong.");
    });
};


  return (
    <div className="w-[90%] mx-auto mt-10 px-6 py-14 bg-[#917843] rounded-xl shadow gap-6 flex flex-col items-center">
      <h3 className="kanit-bold text-gray-100 text-4xl">Inizia ora la tua analisi musicale</h3>
      <p className="font-semibold text-2xl text-gray-300">Scegli come vuoi condividere i tuoi gusti musicali con noi</p>
      <div className="flex gap-2 mb-4 p-2 bg-[#282b2e] w-[80%] rounded-lg">
        <button
          className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'playlist_form' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
          onClick={() => setActiveTab('playlist_form')}
        >
          <CirclePlay /> Playlist Spotify
        </button>
        <button
          className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'songs_form' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
          onClick={() => setActiveTab('songs_form')}
        >
          <Music /> Canzoni Preferite
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 w-[80%] text-left">
        {activeTab === 'playlist_form' && (
          <div><p className="font-semibold text-2xl text-gray-100 mb-4">URL della Playlist Spotify</p>
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
          <div><p className="font-semibold text-2xl text-gray-100 mb-4">Le tue 5 canzoni preferite</p>
          <input type="hidden" name="form_type" value="songs_form" />
            <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 1</p>
            <input
            type="text"
            name="song1"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={songs.song1}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 2</p>
            <input
            type="text"
            name="song2"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={songs.song2}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 3</p>
            <input
            type="text"
            name="song3"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={songs.song3}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 4</p>
            <input
            type="text"
            name="song4"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={songs.song4}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 5</p>
            <input
            type="text"
            name="song5"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={songs.song5}
            onChange={handleChange} required
          />
          </div>
        )}

        <button
          type="submit"
          className="w-full bg-[#1DB954] text-white py-2 rounded hover:bg-green-600"
        >
          Invia
        </button>

        {error && <p style={{ color: 'red' }}>{error}</p>}
        {result && 
        <div>
          <h3 className="text-left kanit-bold text-2xl">Your Type is...</h3>
          <Type0 />
        </div>
        }
      </form>
    </div>
  );
}


export default UploadForm;
