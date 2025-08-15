'use client';

import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Checkbox,
  CheckboxGroup,
  Container,
  FormControl,
  FormLabel,
  Heading,
  NumberInput,
  NumberInputField,
  Select,
  SimpleGrid,
  Stack,
  Text,
  useToast,
  VStack
} from '@chakra-ui/react';
import axios from 'axios';
import { useRouter } from 'next/navigation';

const ALLERGIES = ['Gluten', 'Lactose', 'Œufs', 'Fruits à coque', 'Poisson', 'Crustacés'];
const AVERSIONS = ['Épinards', 'Brocoli', 'Poisson', 'Viande rouge', 'Champignons', 'Fromage'];
const GOALS = ['Améliorer la concentration', 'Booster la mémoire', 'Réduire le stress', "Augmenter l'énergie", 'Améliorer le sommeil'];

export default function ProfilePage() {
  const toast = useToast();
  const router = useRouter();
  const [form, setForm] = useState({
    age: '', gender: '', weight: '', height: '',
    activity_level: 'moderate', sleep_hours: '', stress_level: ''
  });
  const [allergies, setAllergies] = useState([]);
  const [aversions, setAversions] = useState([]);
  const [goals, setGoals] = useState([]);
  const [loading, setLoading] = useState(false);

  // Redirige vers /login si pas connecté
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (!token) {
      router.push('/login');
    }
  }, [router]);

  const setNum = (k) => (v) => setForm(s => ({ ...s, [k]: v }));
  const setStr = (k) => (e) => setForm(s => ({ ...s, [k]: e.target.value }));

  const submit = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const payload = {
        ...form,
        age: Number(form.age),
        weight: Number(form.weight),
        height: Number(form.height),
        sleep_hours: Number(form.sleep_hours),
        stress_level: Number(form.stress_level),
        allergies,
        food_aversions: aversions,
        brain_goals: goals
      };
      await axios.put(
        `${process.env.NEXT_PUBLIC_API_URL}/api/users/profile`,
        payload,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast({
        title: 'Profil mis à jour',
        status: 'success',
        duration: 3000,
        isClosable: true
      });
      router.push('/dashboard');
    } catch (e) {
      toast({
        title: 'Erreur',
        description: e.response?.data?.error || e.message,
        status: 'error',
        duration: 5000,
        isClosable: true
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="4xl" py={10}>
      <VStack align="stretch" spacing={8}>
        <Heading>Créer / Mettre à jour votre profil</Heading>

        {/* Informations de base */}
        <Box p={6} borderWidth="1px" borderRadius="lg">
          <Heading size="md" mb={4}>Informations de base</Heading>
          <SimpleGrid columns={2} gap={4}>
            <FormControl>
              <FormLabel>Âge</FormLabel>
              <NumberInput min={0} value={form.age} onChange={setNum('age')}>
                <NumberInputField />
              </NumberInput>
            </FormControl>
            <FormControl>
              <FormLabel>Sexe</FormLabel>
              <Select value={form.gender} onChange={setStr('gender')}>
                <option value="" disabled>Sélectionner</option>
                <option value="M">Homme</option>
                <option value="F">Femme</option>
                <option value="Other">Autre</option>
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Poids (kg)</FormLabel>
              <NumberInput min={0} value={form.weight} onChange={setNum('weight')}>
                <NumberInputField />
              </NumberInput>
            </FormControl>
            <FormControl>
              <FormLabel>Taille (cm)</FormLabel>
              <NumberInput min={0} value={form.height} onChange={setNum('height')}>
                <NumberInputField />
              </NumberInput>
            </FormControl>
          </SimpleGrid>
        </Box>

        {/* Style de vie */}
        <Box p={6} borderWidth="1px" borderRadius="lg">
          <Heading size="md" mb={4}>Style de vie</Heading>
          <SimpleGrid columns={3} gap={4}>
            <FormControl>
              <FormLabel>Niveau d'activité</FormLabel>
              <Select value={form.activity_level} onChange={setStr('activity_level')}>
                <option value="sedentary">Sédentaire</option>
                <option value="light">Activité légère</option>
                <option value="moderate">Activité modérée</option>
                <option value="very_active">Très actif</option>
              </Select>
            </FormControl>
            <FormControl>
              <FormLabel>Sommeil (h/nuit)</FormLabel>
              <NumberInput min={0} max={24} value={form.sleep_hours} onChange={setNum('sleep_hours')}>
                <NumberInputField />
              </NumberInput>
            </FormControl>
            <FormControl>
              <FormLabel>Stress (1-10)</FormLabel>
              <NumberInput min={1} max={10} value={form.stress_level} onChange={setNum('stress_level')}>
                <NumberInputField />
              </NumberInput>
            </FormControl>
          </SimpleGrid>
        </Box>

        {/* Préférences alimentaires */}
        <Box p={6} borderWidth="1px" borderRadius="lg">
          <Heading size="md" mb={4}>Préférences alimentaires</Heading>
          <VStack align="stretch" spacing={6}>
            <div>
              <Text fontWeight="semibold" mb={2}>Allergies</Text>
              <CheckboxGroup value={allergies} onChange={setAllergies}>
                <Stack direction="row" wrap="wrap" gap={4}>
                  {ALLERGIES.map(a => <Checkbox key={a} value={a}>{a}</Checkbox>)}
                </Stack>
              </CheckboxGroup>
            </div>
            <div>
              <Text fontWeight="semibold" mb={2}>Aversions</Text>
              <CheckboxGroup value={aversions} onChange={setAversions}>
                <Stack direction="row" wrap="wrap" gap={4}>
                  {AVERSIONS.map(a => <Checkbox key={a} value={a}>{a}</Checkbox>)}
                </Stack>
              </CheckboxGroup>
            </div>
            <div>
              <Text fontWeight="semibold" mb={2}>Objectifs cérébraux</Text>
              <CheckboxGroup value={goals} onChange={setGoals}>
                <Stack direction="row" wrap="wrap" gap={4}>
                  {GOALS.map(g => <Checkbox key={g} value={g}>{g}</Checkbox>)}
                </Stack>
              </CheckboxGroup>
            </div>
          </VStack>
        </Box>

        <Button colorScheme="purple" onClick={submit} isLoading={loading}>
          Sauvegarder mon profil
        </Button>
      </VStack>
    </Container>
  );
}
