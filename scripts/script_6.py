# FRONTEND - Composant ScoreChart
score_chart = """import React from 'react';
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
"""

with open('ScoreChart.jsx', 'w') as f:
    f.write(score_chart)

# FRONTEND - Composant MealPlan
meal_plan = """import React, { useState } from 'react';
import {
  Box,
  VStack,
  HStack,
  Text,
  Badge,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  Button,
  useToast,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  FormControl,
  FormLabel,
  Select,
  NumberInput,
  NumberInputField
} from '@chakra-ui/react';
import axios from 'axios';

export default function MealPlan({ plan }) {
  const [selectedMeal, setSelectedMeal] = useState(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const toast = useToast();
  
  if (!plan || !plan.plan_data) {
    return (
      <Box p={8} textAlign="center" color="gray.500">
        Aucun plan nutritionnel disponible. Générez votre premier plan !
      </Box>
    );
  }
  
  const handleMealConsumed = (dayIndex, mealType, meal) => {
    setSelectedMeal({ dayIndex, mealType, meal });
    onOpen();
  };
  
  const submitConsumedMeal = async (consumedData) => {
    try {
      const token = localStorage.getItem('token');
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}/api/mealplans/consumed`,
        {
          meal_date: new Date().toISOString().split('T')[0],
          meal_type: selectedMeal.mealType,
          food_items: consumedData
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast({
        title: 'Repas enregistré',
        description: 'Votre repas a été pris en compte pour le calcul de votre score',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      
      onClose();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible d\\'enregistrer le repas',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };
  
  const getMealTypeLabel = (mealType) => {
    const labels = {
      breakfast: 'Petit-déjeuner',
      lunch: 'Déjeuner',
      dinner: 'Dîner'
    };
    return labels[mealType] || mealType;
  };
  
  return (
    <>
      <Accordion allowMultiple>
        {plan.plan_data.map((day, dayIndex) => (
          <AccordionItem key={day.day}>
            <AccordionButton>
              <Box flex="1" textAlign="left">
                <Text fontWeight="bold">Jour {day.day}</Text>
                <Text fontSize="sm" color="gray.600">
                  {Object.keys(day).filter(k => k !== 'day').length} repas planifiés
                </Text>
              </Box>
              <AccordionIcon />
            </AccordionButton>
            <AccordionPanel pb={4}>
              <VStack spacing={4} align="stretch">
                {Object.entries(day).filter(([key]) => key !== 'day').map(([mealType, meal]) => (
                  <Box key={mealType} p={4} bg="gray.50" rounded="md">
                    <HStack justify="space-between" mb={2}>
                      <Text fontWeight="semibold">{getMealTypeLabel(mealType)}</Text>
                      <Button 
                        size="sm" 
                        colorScheme="green"
                        onClick={() => handleMealConsumed(dayIndex, mealType, meal)}
                      >
                        J'ai mangé ça
                      </Button>
                    </HStack>
                    
                    {meal.foods && (
                      <Text mb={2}>
                        <Text as="span" fontWeight="medium">Aliments: </Text>
                        {meal.foods.join(', ')}
                      </Text>
                    )}
                    
                    <SimpleGrid columns={4} spacing={2}>
                      <Stat size="sm">
                        <StatLabel>Calories</StatLabel>
                        <StatNumber fontSize="md">{meal.calories?.toFixed(0) || 'N/A'}</StatNumber>
                        <StatHelpText>kcal</StatHelpText>
                      </Stat>
                      
                      <Stat size="sm">
                        <StatLabel>Protéines</StatLabel>
                        <StatNumber fontSize="md">{meal.protein?.toFixed(1) || 'N/A'}</StatNumber>
                        <StatHelpText>g</StatHelpText>
                      </Stat>
                      
                      <Stat size="sm">
                        <StatLabel>Oméga-3</StatLabel>
                        <StatNumber fontSize="md">{meal.omega3?.toFixed(1) || 'N/A'}</StatNumber>
                        <StatHelpText>g</StatHelpText>
                      </Stat>
                      
                      <Stat size="sm">
                        <StatLabel>Magnésium</StatLabel>
                        <StatNumber fontSize="md">{meal.magnesium?.toFixed(0) || 'N/A'}</StatNumber>
                        <StatHelpText>mg</StatHelpText>
                      </Stat>
                    </SimpleGrid>
                  </Box>
                ))}
              </VStack>
            </AccordionPanel>
          </AccordionItem>
        ))}
      </Accordion>
      
      {/* Modal pour enregistrer un repas consommé */}
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Enregistrer votre repas</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <Text>
                Vous avez consommé le {getMealTypeLabel(selectedMeal?.mealType)} prévu ?
              </Text>
              
              <FormControl>
                <FormLabel>Portion consommée</FormLabel>
                <Select defaultValue="100">
                  <option value="25">25% - J'ai goûté</option>
                  <option value="50">50% - J'ai mangé la moitié</option>
                  <option value="75">75% - Presque tout</option>
                  <option value="100">100% - Tout le repas</option>
                </Select>
              </FormControl>
              
              <Text fontSize="sm" color="gray.600">
                Nous utiliserons cette information pour calculer précisément vos apports nutritionnels.
              </Text>
            </VStack>
          </ModalBody>
          
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Annuler
            </Button>
            <Button colorScheme="green" onClick={() => submitConsumedMeal([selectedMeal?.meal])}>
              Enregistrer
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}
"""

with open('MealPlan.jsx', 'w') as f:
    f.write(meal_plan)

print("✅ Composants frontend finalisés :")
print("  - ScoreChart.jsx")
print("  - MealPlan.jsx")