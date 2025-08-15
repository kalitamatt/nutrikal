// backend/routes/users.js

const fp = require('fastify-plugin');
const { supabase } = require('../config/database');
const bcrypt = require('bcryptjs');

async function userRoutes(fastify, options) {
  // Accueil API
  fastify.get('/', async (request, reply) => {
    return { service: 'NUTRIKAL Users API' };
  });

  // Inscription
  fastify.post('/register', async (request, reply) => {
    const { email, password, profile } = request.body;
    if (!email || !password) {
      return reply.code(400).send({ error: 'Email et mot de passe requis' });
    }

    try {
      const hashedPassword = await bcrypt.hash(password, 10);
      const { data: user, error: userError } = await supabase
        .from('users')
        .insert([{ email, password_hash: hashedPassword }])
        .select()
        .single();
      if (userError) throw userError;

      // Si on fournit un objet `profile`, on l’insère
      if (profile) {
        const { error: profileError } = await supabase
          .from('user_profiles')
          .insert([{ user_id: user.id, ...profile }]);
        if (profileError) throw profileError;
      }

      const token = fastify.jwt.sign({ userId: user.id });
      reply.send({
        success: true,
        user: { id: user.id, email: user.email },
        token
      });
    } catch (err) {
      reply.code(400).send({ error: err.message });
    }
  });

  // Connexion
  fastify.post('/login', async (request, reply) => {
    const { email, password } = request.body;
    if (!email || !password) {
      return reply.code(400).send({ error: 'Email et mot de passe requis' });
    }

    try {
      const { data: user, error } = await supabase
        .from('users')
        .select('*')
        .eq('email', email)
        .single();
      if (error || !user) {
        return reply.code(401).send({ error: 'Identifiants invalides' });
      }

      const valid = await bcrypt.compare(password, user.password_hash);
      if (!valid) {
        return reply.code(401).send({ error: 'Identifiants invalides' });
      }

      const token = fastify.jwt.sign({ userId: user.id });
      reply.send({
        success: true,
        user: { id: user.id, email: user.email },
        token
      });
    } catch (err) {
      reply.code(500).send({ error: err.message });
    }
  });

  // Middleware d’authentification
  fastify.decorate('authenticate', async (request, reply) => {
    try {
      await request.jwtVerify();
    } catch {
      reply.code(401).send({ error: 'Token invalide' });
    }
  });

  // Obtenir profil (protégé)
  fastify.get(
    '/profile',
    { preHandler: [fastify.authenticate] },
    async (request, reply) => {
      try {
        const { data: profile, error } = await supabase
          .from('user_profiles')
          .select('*')
          .eq('user_id', request.user.userId)
          .single();
        if (error) throw error;
        reply.send({ profile });
      } catch (err) {
        reply.code(500).send({ error: err.message });
      }
    }
  );

  // Mettre à jour profil (protégé)
  fastify.put(
    '/profile',
    { preHandler: [fastify.authenticate] },
    async (request, reply) => {
      try {
        const { data: profile, error } = await supabase
          .from('user_profiles')
          .update(request.body)
          .eq('user_id', request.user.userId)
          .select()
          .single();
        if (error) throw error;
        reply.send({ profile });
      } catch (err) {
        reply.code(500).send({ error: err.message });
      }
    }
  );
}

module.exports = fp(userRoutes);
