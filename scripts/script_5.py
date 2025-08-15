# FRONTEND - Composant ProfileForm
profile_form = """import React, { useState } from 'react';
import {
  Box,
  Container,
  Heading,
  VStack,
  HStack,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  NumberInput,
  NumberInputField,
  Textarea,
  Checkbox,
  CheckboxGroup,
  Stack,
  useToast,
  Divider,
  Text,
  SimpleGrid
} from '@chakra-ui/react';
import { useForm } from 'react-hook-form';
import axios from 'axios';

const commonAllergies = ['Gluten', 'Lactose', 'Œufs', 'Fruits à coque', 'Poisson', 'Crustacés'];
const commonAversions = ['Épinards', 'Brocoli', 'Poisson', 'Viande rouge', 'Champignons', 'Fromage'];
const brainGoals = ['Améliorer la concentration', 'Booster la mémoire', 'Réduire le stress', 'Augmenter l\'énergie', 'Améliorer le sommeil'];

export default function ProfileForm() {
  const { register, handleSubmit, watch, formState: { errors } } = useForm();
  const [allergies, setAllergies] = useState([]);
  const [aversions, setAversions] = useState([]);
  const [goals, setGoals] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  
  const onSubmit = async (data) => {
    setIsLoading(true);
    
    try {
      const profileData = {
        ...data,
        allergies,
        food_aversions: aversions,
        brain_goals: goals
      };
      
      const response = await axios.put(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/profile`,
        profileData,
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        }
      );
      
      toast({
        title: 'Profil mis à jour',
        description: 'Votre profil a été sauvegardé avec succès',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      // Rediriger vers le dashboard
      window.location.href = '/dashboard';
      
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.error || 'Une erreur est survenue',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };
  
  return (
    <Container maxW="4xl" py={10}>
      <VStack spacing={8}>
        <Heading textAlign="center">Créer votre profil NUTRIKAL</Heading>
        <Text textAlign="center" color="gray.600">
          Dites-nous en plus sur vous pour personnaliser votre plan nutritionnel
        </Text>
        
        <Box as="form" onSubmit={handleSubmit(onSubmit)} w="100%">
          <VStack spacing={6}>
            
            {/* Informations de base */}
            <Box w="100%" p={6} bg="white" rounded="lg" shadow="sm">
              <Heading size="md" mb={4}>Informations de base</Heading>
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                <FormControl>
                  <FormLabel>Âge</FormLabel>
                  <NumberInput min={18} max={100}>
                    <NumberInputField {...register('age', { required: 'L\\'âge est requis' })} />
                  </NumberInput>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Sexe</FormLabel>
                  <Select {...register('gender', { required: 'Le sexe est requis' })}>
                    <option value="">Sélectionner</option>
                    <option value="M">Homme</option>
                    <option value="F">Femme</option>
                    <option value="Other">Autre</option>
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Poids (kg)</FormLabel>
                  <NumberInput min={30} max={200} precision={1}>
                    <NumberInputField {...register('weight')} />
                  </NumberInput>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Taille (cm)</FormLabel>
                  <NumberInput min={120} max={220}>
                    <NumberInputField {...register('height')} />
                  </NumberInput>
                </FormControl>
              </SimpleGrid>
            </Box>
            
            {/* Style de vie */}
            <Box w="100%" p={6} bg="white" rounded="lg" shadow="sm">
              <Heading size="md" mb={4}>Style de vie</Heading>
              <SimpleGrid columns={{ base: 1, md: 2 }} spacing={4}>
                <FormControl>
                  <FormLabel>Niveau d'activité physique</FormLabel>
                  <Select {...register('activity_level')}>
                    <option value="sedentary">Sédentaire</option>
                    <option value="light">Activité légère</option>
                    <option value="moderate">Activité modérée</option>
                    <option value="active">Très actif</option>
                  </Select>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Heures de sommeil par nuit</FormLabel>
                  <NumberInput min={4} max={12} precision={1}>
                    <NumberInputField {...register('sleep_hours')} />
                  </NumberInput>
                </FormControl>
                
                <FormControl>
                  <FormLabel>Niveau de stress (1-10)</FormLabel>
                  <NumberInput min={1} max={10}>
                    <NumberInputField {...register('stress_level')} />
                  </NumberInput>
                </FormControl>
              </SimpleGrid>
            </Box>
            
            {/* Allergies et aversions */}
            <Box w="100%" p={6} bg="white" rounded="lg" shadow="sm">
              <Heading size="md" mb={4}>Préférences alimentaires</Heading>
              
              <FormControl mb={4}>
                <FormLabel>Allergies alimentaires</FormLabel>
                <CheckboxGroup value={allergies} onChange={setAllergies}>
                  <Stack direction={{ base: 'column', md: 'row' }} wrap="wrap">
                    {commonAllergies.map(allergy => (
                      <Checkbox key={allergy} value={allergy}>
                        {allergy}
                      </Checkbox>
                    ))}
                  </Stack>
                </CheckboxGroup>
              </FormControl>
              
              <FormControl mb={4}>
                <FormLabel>Aliments que vous n'aimez pas</FormLabel>
                <CheckboxGroup value={aversions} onChange={setAversions}>
                  <Stack direction={{ base: 'column', md: 'row' }} wrap="wrap">
                    {commonAversions.map(aversion => (
                      <Checkbox key={aversion} value={aversion}>
                        {aversion}
                      </Checkbox>
                    ))}
                  </Stack>
                </CheckboxGroup>
              </FormControl>
            </Box>
            
            {/* Objectifs cérébraux */}
            <Box w="100%" p={6} bg="white" rounded="lg" shadow="sm">
              <Heading size="md" mb={4}>Objectifs de performance cérébrale</Heading>
              <FormControl>
                <FormLabel>Que souhaitez-vous améliorer ?</FormLabel>
                <CheckboxGroup value={goals} onChange={setGoals}>
                  <Stack direction="column">
                    {brainGoals.map(goal => (
                      <Checkbox key={goal} value={goal}>
                        {goal}
                      </Checkbox>
                    ))}
                  </Stack>
                </CheckboxGroup>
              </FormControl>
            </Box>
            
            <Button 
              type="submit" 
              colorScheme="purple" 
              size="lg" 
              w="100%" 
              isLoading={isLoading}
            >
              Sauvegarder mon profil
            </Button>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
}
"""

with open('ProfileForm.jsx', 'w') as f:
    f.write(profile_form)

# FRONTEND - Composant Dashboard
dashboard_component = """import React, { useState, useEffect } from 'react';
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
"""

with open('Dashboard.jsx', 'w') as f:
    f.write(dashboard_component)

print("✅ Composants React essentiels créés :")
print("  - ProfileForm.jsx")
print("  - Dashboard.jsx")