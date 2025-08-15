// backend/server.js

const fastify = require('fastify')({ logger: true });
require('dotenv').config();

// CORS pour autoriser le frontend
fastify.register(require('@fastify/cors'), {
  origin: process.env.FRONTEND_URL || 'http://localhost:3000'
});

// JWT pour l’authentification
fastify.register(require('@fastify/jwt'), {
  secret: process.env.JWT_SECRET || 'nutrikal-super-secret-key'
});

// Routes
fastify.register(require('./routes/users'), { prefix: '/api/users' });
fastify.register(require('./routes/mealplans'), { prefix: '/api/mealplans' });
fastify.register(require('./routes/scores'), { prefix: '/api/scores' });

// Route de santé
fastify.get('/health', async (request, reply) => {
  return {
    status: 'healthy',
    service: 'NUTRIKAL API',
    timestamp: new Date().toISOString()
  };
});

// Démarrage du serveur
const start = async () => {
  try {
    const port = Number(process.env.PORT) || 3001;
    await fastify.listen({ port, host: '0.0.0.0' });
    fastify.log.info(`🚀 NUTRIKAL API démarrée sur http://0.0.0.0:${port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
