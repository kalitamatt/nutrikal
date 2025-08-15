# FRONTEND - Package.json
frontend_package = {
    "name": "nutrikal-frontend",
    "version": "1.0.0",
    "description": "Frontend pour NUTRIKAL - Plateforme de nutrition cérébrale",
    "scripts": {
        "dev": "next dev",
        "build": "next build",
        "start": "next start",
        "lint": "next lint"
    },
    "dependencies": {
        "next": "14.0.3",
        "react": "^18.2.0",
        "react-dom": "^18.2.0",
        "@chakra-ui/react": "^2.8.2",
        "@emotion/react": "^11.11.1",
        "@emotion/styled": "^11.11.0",
        "framer-motion": "^10.16.5",
        "@chakra-ui/icons": "^2.1.1",
        "@supabase/supabase-js": "^2.38.4",
        "recharts": "^2.8.0",
        "axios": "^1.6.2",
        "react-hook-form": "^7.47.0",
        "react-datepicker": "^4.25.0",
        "js-cookie": "^3.0.5"
    },
    "devDependencies": {
        "@types/node": "^20.9.0",
        "@types/react": "^18.2.37",
        "@types/react-dom": "^18.2.15",
        "eslint": "^8.53.0",
        "eslint-config-next": "14.0.3",
        "typescript": "^5.2.2"
    }
}

with open('frontend_package.json', 'w') as f:
    f.write(json.dumps(frontend_package, indent=2))

# FRONTEND - Configuration Next.js
nextjs_config = """/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_SUPABASE_URL: process.env.NEXT_PUBLIC_SUPABASE_URL,
    NEXT_PUBLIC_SUPABASE_ANON_KEY: process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3001'
  }
}

module.exports = nextConfig
"""

with open('next.config.js', 'w') as f:
    f.write(nextjs_config)

# FRONTEND - Configuration Supabase
supabase_config = """import { createClient } from '@supabase/supabase-js'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Variables d\\'environnement Supabase manquantes')
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
"""

with open('supabase_lib.js', 'w') as f:
    f.write(supabase_config)

# FRONTEND - Page principale
index_page = """import React from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  Button,
  VStack,
  HStack,
  Icon,
  useColorModeValue,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText
} from '@chakra-ui/react';
import { Brain, Activity, Target } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const bgColor = useColorModeValue('gray.50', 'gray.900');
  const cardBg = useColorModeValue('white', 'gray.800');
  
  return (
    <Box bg={bgColor} minH="100vh">
      <Container maxW="7xl" py={20}>
        {/* Hero Section */}
        <VStack spacing={8} textAlign="center" mb={16}>
          <Icon as={Brain} boxSize={16} color="purple.500" />
          <Heading size="2xl" fontWeight="bold">
            NUTRIKAL
          </Heading>
          <Text fontSize="xl" color="gray.600" maxW="2xl">
            Optimisez votre performance cérébrale grâce à une nutrition personnalisée. 
            Découvrez comment votre alimentation peut booster votre cerveau de dirigeant.
          </Text>
          <HStack spacing={4}>
            <Link href="/profile">
              <Button colorScheme="purple" size="lg">
                Commencer mon profil
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button variant="outline" size="lg">
                Voir mon tableau de bord
              </Button>
            </Link>
          </HStack>
        </VStack>
        
        {/* Features */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8} mb={16}>
          <Box bg={cardBg} p={6} rounded="lg" shadow="md">
            <VStack spacing={4}>
              <Icon as={Target} boxSize={10} color="purple.500" />
              <Heading size="md">Plan Personnalisé</Heading>
              <Text textAlign="center" color="gray.600">
                Un plan nutritionnel adapté à votre profil, vos objectifs et vos contraintes alimentaires.
              </Text>
            </VStack>
          </Box>
          
          <Box bg={cardBg} p={6} rounded="lg" shadow="md">
            <VStack spacing={4}>
              <Icon as={Activity} boxSize={10} color="green.500" />
              <Heading size="md">Suivi Intelligent</Heading>
              <Text textAlign="center" color="gray.600">
                Une IA locale analyse vos repas et calcule votre score de performance cérébrale quotidien.
              </Text>
            </VStack>
          </Box>
          
          <Box bg={cardBg} p={6} rounded="lg" shadow="md">
            <VStack spacing={4}>
              <Icon as={Brain} boxSize={10} color="blue.500" />
              <Heading size="md">Performance Optimisée</Heading>
              <Text textAlign="center" color="gray.600">
                Maximisez votre concentration, mémoire et énergie mentale grâce à des recommendations scientifiques.
              </Text>
            </VStack>
          </Box>
        </SimpleGrid>
        
        {/* Stats Example */}
        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={8}>
          <Stat bg={cardBg} p={6} rounded="lg" shadow="md">
            <StatLabel>Score moyen</StatLabel>
            <StatNumber>85.2</StatNumber>
            <StatHelpText>+12% ce mois</StatHelpText>
          </Stat>
          
          <Stat bg={cardBg} p={6} rounded="lg" shadow="md">
            <StatLabel>Adhérence au plan</StatLabel>
            <StatNumber>92%</StatNumber>
            <StatHelpText>Excellent suivi</StatHelpText>
          </Stat>
          
          <Stat bg={cardBg} p={6} rounded="lg" shadow="md">
            <StatLabel>Objectifs atteints</StatLabel>
            <StatNumber>7/8</StatNumber>
            <StatHelpText>Cette semaine</StatHelpText>
          </Stat>
        </SimpleGrid>
      </Container>
    </Box>
  );
}
"""

with open('index_page.js', 'w') as f:
    f.write(index_page)

print("✅ Frontend Next.js créé :")
print("  - frontend_package.json")
print("  - next.config.js")
print("  - supabase_lib.js")
print("  - index_page.js")