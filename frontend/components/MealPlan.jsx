import React, { useState } from 'react';
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
        description: 'Impossible d\'enregistrer le repas',
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
