'use client';

import React, { useEffect, useState } from 'react';
import {
  Alert, AlertIcon, Box, Button, Card, CardBody, Container, Heading, HStack,
  SimpleGrid, Spinner, Stat, StatHelpText, StatLabel, StatNumber, Text, VStack, useToast
} from '@chakra-ui/react';
import axios from 'axios';

export default function DashboardPage() {
  const [profile, setProfile] = useState(null);
  const [scores, setScores] = useState([]);
  const [plan, setPlan] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => { load(); }, []);

  async function load() {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Veuillez vous connecter.');
      const headers = { Authorization: `Bearer ${token}` };

      const [p, s, pl, st] = await Promise.all([
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/users/profile`, { headers }),
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/scores?from_date=${dateMinus(30)}`, { headers }),
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/mealplans/active`, { headers }),
        axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/scores/stats`, { headers }),
      ]);

      setProfile(p.data.profile);
      setScores(s.data.scores || []);
      setPlan(pl.data.plan || null);
      setStats(st.data.stats || null);
    } catch (e) {
      toast({ title: 'Erreur de chargement', description: e.response?.data?.error || e.message, status: 'error', duration: 5000, isClosable: true });
    } finally {
      setLoading(false);
    }
  }

  async function generatePlan() {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/mealplans/generate`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setPlan(res.data.plan);
      toast({ title: 'Plan généré', status: 'success', duration: 3000, isClosable: true });
    } catch (e) {
      toast({ title: 'Erreur', description: e.response?.data?.error || 'Impossible de générer le plan', status: 'error', duration: 5000, isClosable: true });
    }
  }

  if (loading) {
    return (
      <Container maxW="5xl" py={12}><HStack><Spinner /><Text>Chargement…</Text></HStack></Container>
    );
  }

  if (!profile) {
    return (
      <Container maxW="3xl" py={12}>
        <Alert status="warning"><AlertIcon />Complétez votre profil pour accéder au dashboard.</Alert>
        <Button mt={4} as="a" href="/profile" colorScheme="purple">Aller au profil</Button>
      </Container>
    );
  }

  return (
    <Container maxW="6xl" py={10}>
      <VStack align="stretch" spacing={8}>
        <HStack justify="space-between">
          <Heading>Votre tableau de bord</Heading>
          <Button onClick={generatePlan} colorScheme="purple">Générer un nouveau plan</Button>
        </HStack>

        <SimpleGrid columns={3} gap={6}>
          <Stat border="1px solid #eee" borderRadius="md" p={4}>
            <StatLabel>Score moyen</StatLabel>
            <StatNumber>{stats?.average_score?.toFixed(1) ?? '—'}</StatNumber>
            <StatHelpText>Tendance: {stats?.trend ?? '—'}</StatHelpText>
          </Stat>
          <Stat border="1px solid #eee" borderRadius="md" p={4}>
            <StatLabel>Meilleur score</StatLabel>
            <StatNumber>{stats?.best_score?.toFixed(1) ?? '—'}</StatNumber>
            <StatHelpText>Record personnel</StatHelpText>
          </Stat>
          <Stat border="1px solid #eee" borderRadius="md" p={4}>
            <StatLabel>Jours suivis</StatLabel>
            <StatNumber>{stats?.total_days ?? 0}</StatNumber>
            <StatHelpText>30 derniers jours</StatHelpText>
          </Stat>
        </SimpleGrid>

        <Card>
          <CardBody>
            <Heading size="md" mb={3}>Plan nutritionnel</Heading>
            {!plan ? (
              <Text>Aucun plan actif. Cliquez sur “Générer un nouveau plan”.</Text>
            ) : (
              <VStack align="stretch" spacing={3}>
                <Text>Créé le {new Date(plan.created_at).toLocaleDateString()}</Text>
                <SimpleGrid columns={3} gap={4}>
                  {plan.plan_data?.slice(0, 3).map((day) => (
                    <Box key={day.day} border="1px solid #eee" p={3} borderRadius="md">
                      <Text fontWeight="bold">Jour {day.day}</Text>
                      {['breakfast', 'lunch', 'dinner'].map((m) => (
                        <Text key={m}>{m}: {Array.isArray(day[m]?.foods) ? day[m].foods.join(', ') : '—'}</Text>
                      ))}
                    </Box>
                  ))}
                </SimpleGrid>
                <Text fontSize="sm" color="gray.500">Aperçu des 3 premiers jours.</Text>
              </VStack>
            )}
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <Heading size="md" mb={3}>Historique des scores</Heading>
            {scores.length === 0 ? (
              <Text>Aucune donnée pour l’instant.</Text>
            ) : (
              <SimpleGrid columns={3} gap={3}>
                {scores.slice(-9).map(s => (
                  <Box key={s.score_date} border="1px solid #eee" p={3} borderRadius="md">
                    <Text fontWeight="bold">{new Date(s.score_date).toLocaleDateString()}</Text>
                    <Text>Global: {s.daily_score}</Text>
                    <Text>Adhérence: {s.adherence_score}</Text>
                    <Text>Nutrition: {s.nutrition_score}</Text>
                  </Box>
                ))}
              </SimpleGrid>
            )}
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
}
function dateMinus(days) {
  const d = new Date();
  d.setDate(d.getDate() - days);
  return d.toISOString().split('T')[0];
}
