import { useState } from 'react';
import { Music } from 'lucide-react';
import { CirclePlay } from 'lucide-react';

function UploadForm() {
  const [activeTab, setActiveTab] = useState('playlist');
  const [formData, setFormData] = useState({
    option1Field: '',
    option2Field: '',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (activeTab === 'playlist') {
      console.log('Submitting Option 1:', formData.option1Field);
    } else {
      console.log('Submitting Option 2:', formData.option2Field);
    }
  };

  return (
    <div className="w-[90%] mx-auto mt-10 px-6 py-14 bg-[#917843] rounded-xl shadow gap-6 flex flex-col items-center">
      <h3 className="font-bold text-gray-100 text-4xl">Inizia ora la tua analisi musicale</h3>
      <p className="font-semibold text-2xl text-gray-300">Scegli come vuoi condividere i tuoi gusti musicali con noi</p>
      <div className="flex gap-2 mb-4 p-2 bg-[#282b2e] w-[80%] rounded-lg">
        <button
          className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'playlist' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
          onClick={() => setActiveTab('playlist')}
        >
          <CirclePlay /> Playlist Spotify
        </button>
        <button
          className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'songs' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
          onClick={() => setActiveTab('songs')}
        >
          <Music /> Canzoni Preferite
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6 w-[80%] text-left">
        {activeTab === 'playlist' && (
          <div><p className="font-semibold text-2xl text-gray-100 mb-4">URL della Playlist Spotify</p>
          <input
            type="text"
            name="playlistField"
            placeholder="https://open.spotify.com/playlists/..."
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.playlistField}
            onChange={handleChange} required
          /></div>
        )}

        {activeTab === 'songs' && (
          <div><p className="font-semibold text-2xl text-gray-100 mb-4">Le tue 5 canzoni preferite</p>
            <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 1</p>
            <input
            type="text"
            name="song1"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.song1Field}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 2</p>
            <input
            type="text"
            name="song2"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.song2Field}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 3</p>
            <input
            type="text"
            name="song3"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.song3Field}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 4</p>
            <input
            type="text"
            name="song4"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.song4Field}
            onChange={handleChange} required
          />
          <p className="font-semibold text-lg text-gray-300 mb-2">Canzone 5</p>
            <input
            type="text"
            name="song5"
            placeholder="Artista - Titolo Canzone"
            className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
            value={formData.song5Field}
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
      </form>
    </div>
  );
}


export default UploadForm;
