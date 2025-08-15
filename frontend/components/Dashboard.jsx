import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Button,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Card,
  CardBody,
  Text,
  Progress,
  useToast,
  Spinner,
  Alert,
  AlertIcon
} from '@chakra-ui/react';
import axios from 'axios';
import ScoreChart from './ScoreChart';
import MealPlan from './MealPlan';

export default function Dashboard() {
  const [profile, setProfile] = useState(null);
  const [scores, setScores] = useState([]);
  const [currentPlan, setCurrentPlan] = useState(null);
  const [stats, setStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      const headers = { Authorization: `Bearer ${token}` };

      // Charger le profil
      const profileRes = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/users/profile`, { headers });
      setProfile(profileRes.data.profile);

      // Charger les scores des 30 derniers jours
      const scoresRes = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/scores?from_date=${getDateXDaysAgo(30)}`, { headers });
      setScores(scoresRes.data.scores);

      // Charger le plan actif
      const planRes = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/mealplans/active`, { headers });
      setCurrentPlan(planRes.data.plan);

      // Charger les statistiques
      const statsRes = await axios.get(`${process.env.NEXT_PUBLIC_API_URL}/api/scores/stats`, { headers });
      setStats(statsRes.data.stats);

    } catch (error) {
      toast({
        title: 'Erreur de chargement',
        description: error.response?.data?.error || 'Impossible de charger les données',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const generateNewPlan = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/mealplans/generate`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setCurrentPlan(response.data.plan);
      toast({
        title: 'Nouveau plan généré',
        description: 'Votre plan nutritionnel a été mis à jour',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });

    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.error || 'Impossible de générer le plan',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (isLoading) {
    return (
      <Container maxW="7xl" py={10}>
        <VStack>
          <Spinner size="xl" />
          <Text>Chargement de votre tableau de bord...</Text>
        </VStack>
      </Container>
    );
  }

  if (!profile) {
    return (
      <Container maxW="7xl" py={10}>
        <Alert status="warning">
          <AlertIcon />
          Veuillez d'abord compléter votre profil pour accéder au tableau de bord.
        </Alert>
      </Container>
    );
  }

  return (
    <Container maxW="7xl" py={10}>
      <VStack spacing={8}>

        {/* Header */}
        <HStack justify="space-between" w="100%">
          <VStack align="start" spacing={0}>
            <Heading>Bonjour ! 👋</Heading>
            <Text color="gray.600">Voici votre tableau de bord NUTRIKAL</Text>
          </VStack>
          <Button colorScheme="purple" onClick={generateNewPlan}>
            Générer un nouveau plan
          </Button>
        </HStack>

        {/* Statistiques principales */}
        <SimpleGrid columns={{ base: 1, md: 4 }} spacing={6} w="100%">
          <Stat bg="white" p={6} rounded="lg" shadow="sm">
            <StatLabel>Score moyen</StatLabel>
            <StatNumber>{stats?.average_score?.toFixed(1) || 'N/A'}</StatNumber>
            <StatHelpText>
              {stats?.trend === 'improving' && <StatArrow type="increase" />}
              {stats?.trend === 'declining' && <StatArrow type="decrease" />}
              {stats?.trend || 'stable'}
            </StatHelpText>
          </Stat>

          <Stat bg="white" p={6} rounded="lg" shadow="sm">
            <StatLabel>Meilleur score</StatLabel>
            <StatNumber>{stats?.best_score?.toFixed(1) || 'N/A'}</StatNumber>
            <StatHelpText>Record personnel</StatHelpText>
          </Stat>

          <Stat bg="white" p={6} rounded="lg" shadow="sm">
            <StatLabel>Jours suivis</StatLabel>
            <StatNumber>{stats?.total_days || 0}</StatNumber>
            <StatHelpText>Total</StatHelpText>
          </Stat>

          <Stat bg="white" p={6} rounded="lg" shadow="sm">
            <StatLabel>Objectifs atteints</StatLabel>
            <StatNumber>
              {profile?.brain_goals?.length || 0}/{brainGoals.length}
            </StatNumber>
            <StatHelpText>Cette semaine</StatHelpText>
          </Stat>
        </SimpleGrid>

        {/* Graphique des scores */}
        <Card w="100%">
          <CardBody>
            <Heading size="md" mb={4}>Évolution de vos scores</Heading>
            <ScoreChart data={scores} />
          </CardBody>
        </Card>

        {/* Plan nutritionnel */}
        <Card w="100%">
          <CardBody>
            <HStack justify="space-between" mb={4}>
              <Heading size="md">Votre plan nutritionnel</Heading>
              {currentPlan && (
                <Text fontSize="sm" color="gray.500">
                  Créé le {new Date(currentPlan.created_at).toLocaleDateString()}
                </Text>
              )}
            </HStack>
            <MealPlan plan={currentPlan} />
          </CardBody>
        </Card>

        {/* Objectifs de la semaine */}
        <Card w="100%">
          <CardBody>
            <Heading size="md" mb={4}>Objectifs de la semaine</Heading>
            <VStack spacing={3} align="stretch">
              {profile?.brain_goals?.map((goal, index) => (
                <Box key={index}>
                  <HStack justify="space-between" mb={1}>
                    <Text>{goal}</Text>
                    <Text fontSize="sm" color="gray.500">
                      {Math.floor(Math.random() * 30 + 70)}%
                    </Text>
                  </HStack>
                  <Progress 
                    value={Math.floor(Math.random() * 30 + 70)} 
                    colorScheme="purple" 
                    size="sm" 
                  />
                </Box>
              ))}
            </VStack>
          </CardBody>
        </Card>
      </VStack>
    </Container>
  );
}

function getDateXDaysAgo(days) {
  const date = new Date();
  date.setDate(date.getDate() - days);
  return date.toISOString().split('T')[0];
}
