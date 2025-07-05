import ResultChart from "../ResultChart";

function Type0(){

    return(
        <div className="bg-[url(../../../public/red.png)] w-[90%] mx-auto px-8 py-10 rounded-xl text-left">
            <h2 className="kanit-black text-gray-100 text-5xl mb-4">The Melancholy Dancer</h2>
            <div className="flex gap-4 justify-between items-start w-full">
                <div className="text-gray-200 text-xl w-[50%] flex flex-col gap-10">
                    <p>
                        <span className="font-semibold">Danceability:</span> 0.7<br />
                        <span className="font-semibold">Energy:</span> 0.7<br />
                        <span className="font-semibold">Valence:</span> 0.7<br />
                        <span className="font-semibold">Instrumentalness:</span> 0.7<br />
                        <span className="font-semibold">Acousticness:</span> 0.7<br />
                    </p>
                    <p className="mt-6">A complex blend of rhythm and emotion. You love music with movement, yet your playlists reveal a subtle sadness or introspection beneath the surface, often favoring tracks that are danceable but emotionally layered.</p>
                </div>
                <ResultChart />
            </div>
        </div>
    )
}

export default Type0;