import ResultChart from "./ResultChart";

const Type = ({ features, data }) => {

    return(
        <div style={{ backgroundImage: `url(../../../public/${data.color}.png)`, width: 'min(1000px, 90%)' }}
            className="mx-auto p-10 rounded-xl text-left">
            <h2 className="kanit-black text-gray-100 text-5xl mb-4">{data.title}</h2>
            <div className="flex gap-4 justify-between items-start w-full">
                <div className="text-gray-200 text-xl w-[50%] flex flex-col gap-4">
                    <p>
                        <span className="font-semibold">Danceability:</span> {features.danceability.toFixed(2)}<br />
                        <span className="font-semibold">Energy:</span> {features.energy.toFixed(2)}<br />
                        <span className="font-semibold">Valence:</span> {features.valence.toFixed(2)}<br />
                        <span className="font-semibold">Instrumentalness:</span> {features.instrumentalness.toFixed(2)}<br />
                        <span className="font-semibold">Acousticness:</span> {features.acousticness.toFixed(2)}<br />
                    </p>
                    <p className="my-4">{data.description}</p>
                    <p><span className="font-semibold">Famous Songs Related:</span><br />
                        {data.songs} 
                    </p>
                </div>
                <ResultChart data={features}/>
            </div>
        </div>
    )
}

export default Type;