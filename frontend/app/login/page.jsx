'use client';
import React, { useState } from 'react';
import {
  Box, Button, Container, FormControl, FormLabel,
  Heading, HStack, Input, Text, useToast, VStack
} from '@chakra-ui/react';
import axios from 'axios';

export default function LoginPage() {
  const toast = useToast();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [isLogin, setIsLogin] = useState(true);

  const submit = async () => {
    if (!email || !password) {
      return toast({
        title: 'Erreur',
        description: 'Email et mot de passe requis',
        status: 'error',
        duration: 3000,
        isClosable: true
      });
    }
    setLoading(true);
    try {
      const endpoint = isLogin ? '/api/users/login' : '/api/users/register';
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_URL}${endpoint}`,
        { email, password }
      );
      const { token } = res.data;
      if (token) {
        localStorage.setItem('token', token);
        toast({
          title: 'Succès',
          description: isLogin ? 'Connexion réussie' : 'Compte créé',
          status: 'success',
          duration: 3000,
          isClosable: true
        });
        window.location.href = '/profile';
      }
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
    <Container maxW="md" py={12}>
      <VStack spacing={6}>
        <Heading>{isLogin ? 'Connexion' : 'Inscription'}</Heading>
        <Box w="full" p={6} borderWidth="1px" borderRadius="lg">
          <VStack spacing={4}>
            <FormControl>
              <FormLabel>Email</FormLabel>
              <Input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="votre@email.com"
              />
            </FormControl>
            <FormControl>
              <FormLabel>Mot de passe</FormLabel>
              <Input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
              />
            </FormControl>
            <Button
              w="full"
              colorScheme="purple"
              onClick={submit}
              isLoading={loading}
            >
              {isLogin ? 'Se connecter' : "S'inscrire"}
            </Button>
          </VStack>
        </Box>
        <HStack>
          <Text>
            {isLogin ? "Pas encore de compte ?" : "Déjà un compte ?"}
          </Text>
          <Button
            variant="link"
            colorScheme="purple"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Créer un compte" : 'Se connecter'}
          </Button>
        </HStack>
      </VStack>
    </Container>
  );
}
