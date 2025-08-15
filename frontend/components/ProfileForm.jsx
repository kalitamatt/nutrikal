import React, { useState } from 'react';
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
const brainGoals = ['Améliorer la concentration', 'Booster la mémoire', 'Réduire le stress', 'Augmenter l'énergie', 'Améliorer le sommeil'];

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
                    <NumberInputField {...register('age', { required: 'L\'âge est requis' })} />
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
