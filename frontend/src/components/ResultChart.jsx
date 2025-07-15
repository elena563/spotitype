import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';

const ResultChart = ({ features }) => {

  const data = [
    { subject: 'D', value: features.danceability },
    { subject: 'E', value: features.energy },
    { subject: 'V', value: features.valence },
    { subject: 'I', value: features.instrumentalness },
    { subject: 'A', value: features.acousticness },
  ];
  console.log(data);

  return (
    <RadarChart outerRadius={180} width={400} height={450} data={data}>
        <PolarGrid stroke="#d3d3d3" />                    
        <PolarAngleAxis dataKey="subject" stroke="#fff" tick={{ fontSize: 24 }}/> 
        <PolarRadiusAxis domain={[0, 1]} tick={false} axisLine={false} />
        <Radar dataKey="value" stroke="#ffffff" fill="#ffffff" fillOpacity={0.6} strokeWidth={3} />
    </RadarChart>

      );
}

export default ResultChart;