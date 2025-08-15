import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { Box } from '@chakra-ui/react';

export default function ScoreChart({ data = [] }) {

  // Transformer les données pour le graphique
  const chartData = data.map(score => ({
    date: new Date(score.score_date).toLocaleDateString('fr-FR', { 
      month: 'short', 
      day: 'numeric' 
    }),
    'Score global': score.daily_score,
    'Adhérence': score.adherence_score,
    'Nutrition': score.nutrition_score
  }));

  if (chartData.length === 0) {
    return (
      <Box p={8} textAlign="center" color="gray.500">
        Aucune donnée à afficher. Commencez à suivre vos repas pour voir vos scores !
      </Box>
    );
  }

  return (
    <Box h="400px">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            tick={{ fontSize: 12 }}
          />
          <YAxis 
            domain={[0, 100]}
            tick={{ fontSize: 12 }}
          />
          <Tooltip 
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e2e8f0',
              borderRadius: '8px'
            }}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="Score global"
            stroke="#805AD5"
            strokeWidth={3}
            dot={{ fill: '#805AD5', strokeWidth: 2, r: 6 }}
            activeDot={{ r: 8 }}
          />
          <Line
            type="monotone"
            dataKey="Adhérence"
            stroke="#38A169"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
          <Line
            type="monotone"
            dataKey="Nutrition"
            stroke="#3182CE"
            strokeWidth={2}
            strokeDasharray="5 5"
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
}
