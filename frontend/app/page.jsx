'use client';

import { Box, Button, Container, Heading, HStack, SimpleGrid, Text, VStack } from '@chakra-ui/react';
import Link from 'next/link';

export default function HomePage() {
  return (
    <Container maxW="6xl" py={12}>
      <VStack spacing={8} align="start">
        {/* Hero Section */}
        <VStack spacing={4} align="start">
          <Heading size="2xl">NUTRIKAL</Heading>
          <Text fontSize="lg">
            Optimisez votre performance cérébrale grâce à une nutrition personnalisée.
          </Text>
          <HStack spacing={4}>
            <Button as={Link} href="/profile" colorScheme="purple">
              Commencer mon profil
            </Button>
            <Button as={Link} href="/dashboard" variant="outline">
              Voir mon tableau de bord
            </Button>
            <Button as={Link} href="/login" variant="link">
              Connexion
            </Button>
          </HStack>
        </VStack>

        {/* Features */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="full">
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Heading size="md">Plan Personnalisé</Heading>
            <Text mt={2}>Un plan adapté à vos objectifs et contraintes.</Text>
          </Box>
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Heading size="md">Suivi Intelligent</Heading>
            <Text mt={2}>Score de performance cérébrale quotidien.</Text>
          </Box>
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Heading size="md">Performance Optimisée</Heading>
            <Text mt={2}>Concentration, mémoire et énergie.</Text>
          </Box>
        </SimpleGrid>

        {/* Stats */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6} w="full">
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Text fontSize="sm" color="gray.500">Score moyen</Text>
            <Heading size="lg">85.2</Heading>
            <Text color="green.500">+12% ce mois</Text>
          </Box>
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Text fontSize="sm" color="gray.500">Adhérence au plan</Text>
            <Heading size="lg">92%</Heading>
            <Text color="green.500">Excellent suivi</Text>
          </Box>
          <Box p={5} borderWidth="1px" borderRadius="md">
            <Text fontSize="sm" color="gray.500">Objectifs atteints</Text>
            <Heading size="lg">7/8</Heading>
            <Text color="gray.500">Cette semaine</Text>
          </Box>
        </SimpleGrid>
      </VStack>
    </Container>
);
}
