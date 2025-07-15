import { useState } from 'react';
import { CirclePlay, Music } from 'lucide-react';
import Loader from './Loader';
import Type from './Type';

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

  const typeData = [
    {
      color: "red",
      title: "The Melancholy Dancer",
      description: "A complex blend of rhythm and emotion. You love music with movement, yet your playlists reveal a subtle sadness or introspection beneath the surface, often favoring tracks that are danceable but emotionally layered.",
      songs: (
        <>
          Cigarettes After Sex - Apocalypse<br />
          Mitski - Washing Machine Heart<br />
          Mac DeMarco - Chamber Of Reflection 
        </>
      )
    },
    {
      color: "violet",
      title: "The Night Soul",
      description: "Mysterious and magnetic, as a listener you are drawn to depth and emotion. You seek moody, atmospheric tracks with a touch of sensuality—music that feels nocturnal, intimate, and a little rebellious.",
      songs: (
        <>
          Sam Smith, Kim Petras - Unholy<br />
          The Weeknd - Blinding Lights <br />
          The Neighbourhood -  Sweater Weather
        </>
      )
    },
    {
      color: "blue",
      title: "The Deep Nostalgic",
      description: "Emotionally connected to music that resonates with sadness, depth, and memory. You gravitate toward slower, acoustic-heavy tracks with strong emotional undertones, often reflecting on the past through sound.",
      songs: (
        <>
          Tom Odell - Another Love<br />
          Sam Smith - I'm Not The Only One<br />
          Billie Eilish, Khalid - lovely 
        </>
      ) 
    },
    {
      color: "green",
      title: "The Bright Wanderer",
      description: "Energetic yet balanced, you enjoy upbeat, positive tracks that are both danceable and emotionally warm. Your playlists often carry a sense of optimism, exploration, and light-hearted movement.",
      songs: (
        <>
          Ed Sheeran - Shape of You<br />
          Justin Bieber, Daniel Caesar, Giveon - Peaches<br />
          Ariana Grande - positions
        </>
      )   
    },
    {
      color: "orange",
      title: "The Party Animal",
      description: "Always ready for the next big beat. You seek high-energy tracks with loud, fast-paced rhythms and minimal acoustic elements—perfect for dancing, partying, and keeping the vibes high.",
      songs: (
        <>
          Quevedo, Bizarrap - Quevedo Bzrp Music Sessions, Vol. 52<br />
          Beyoncé - CUFF IT<br />
          Nicki Minaj	- Super Freaky Girl 
        </>
      )  
    },
    {
      color: "grey",
      title: "The Ethereal Thinker",
      description: "A quiet soul drawn to introspective and instrumental sounds. Your taste leans toward atmospheric, acoustic tracks with minimal lyrics, often preferring music that evokes space, thought, and emotion without the need for words.",
      songs: (
        <>
          Billie Eilish - everything i wanted<br />
          Yot Club - YKWIM?<br />
          Tom Rosenthal - Lights Are On 
        </>
      )
    }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSongs(prev => ({ ...prev, [name]: value }));
  };


  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    let payload = { form_type: activeTab };

    if (activeTab === "playlist_form") {
      payload.playlistField = playlistField;
    } else if (activeTab === "songs_form") {
      payload = {
        ...payload,
        song1: songs.song1,
        song2: songs.song2,
        song3: songs.song3,
        song4: songs.song4,
        song5: songs.song5,
      };

    }

    fetch("http://localhost:5000/", {
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
        setError(data.error || "Something went wrong.");
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
            onClick={() => setActiveTab('playlist_form')}
          >
            <CirclePlay /> Spotify Playlist 
          </button>
          <button
            className={`flex gap-2 items-center justify-center px-4 py-2 w-[50%] rounded ${activeTab === 'songs_form' ? 'bg-[#1DB954] text-white' : 'bg-[#282b2e] text-[#ff00ba]'}`}
            onClick={() => setActiveTab('songs_form')}
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
              <p className="font-semibold text-lg text-gray-300 mb-2">Song 1</p>
              <input
              type="text"
              name="song1"
              placeholder="Artista - Titolo Canzone"
              className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
              value={songs.song1}
              onChange={handleChange} required
            />
            <p className="font-semibold text-lg text-gray-300 mb-2">Song 2</p>
              <input
              type="text"
              name="song2"
              placeholder="Artista - Titolo Canzone"
              className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
              value={songs.song2}
              onChange={handleChange} required
            />
            <p className="font-semibold text-lg text-gray-300 mb-2">Song 3</p>
              <input
              type="text"
              name="song3"
              placeholder="Artista - Titolo Canzone"
              className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
              value={songs.song3}
              onChange={handleChange} required
            />
            <p className="font-semibold text-lg text-gray-300 mb-2">Song 4</p>
              <input
              type="text"
              name="song4"
              placeholder="Artista - Titolo Canzone"
              className="mb-4 w-full px-4 py-3 rounded bg-[#282b2e] text-[#ff00ba] placeholder-[#ff00ba]"
              value={songs.song4}
              onChange={handleChange} required
            />
            <p className="font-semibold text-lg text-gray-300 mb-2">Song 5</p>
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
