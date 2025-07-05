import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from 'recharts';

const data = [
  { subject: 'D', A: 120 },
  { subject: 'E', A: 98 },
  { subject: 'V', A: 86 },
  { subject: 'I', A: 99 },
  { subject: 'A', A: 85 },
];

function ResultChart() {
  return (
    <RadarChart outerRadius={180} width={400} height={450} data={data}>
        <PolarGrid stroke="#d3d3d3" />                    
        <PolarAngleAxis dataKey="subject" stroke="#fff" tick={{ fontSize: 24 }}/> 
        <Radar dataKey="A" stroke="#ffffff" fill="#ffffff" fillOpacity={0.6} strokeWidth={3} />
    </RadarChart>

      );
}

export default ResultChart;