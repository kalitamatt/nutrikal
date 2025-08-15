# BACKEND - Package.json
backend_package = {
    "name": "nutrikal-backend",
    "version": "1.0.0",
    "description": "Backend API pour NUTRIKAL - Plateforme de nutrition cérébrale",
    "main": "server.js",
    "scripts": {
        "start": "node server.js",
        "dev": "nodemon server.js",
        "test": "jest"
    },
    "dependencies": {
        "fastify": "^4.24.3",
        "@fastify/cors": "^8.4.0",
        "@fastify/jwt": "^7.2.4",
        "@supabase/supabase-js": "^2.38.4",
        "bcrypt": "^5.1.1",
        "dotenv": "^16.3.1",
        "ajv": "^8.12.0"
    },
    "devDependencies": {
        "nodemon": "^3.0.2",
        "jest": "^29.7.0"
    }
}

with open('backend_package.json', 'w') as f:
    f.write(json.dumps(backend_package, indent=2))

# BACKEND - Server principal
server_js = """const fastify = require('fastify')({ logger: true });
const path = require('path');

// Configuration environnement
require('dotenv').config();

// Plugins
fastify.register(require('@fastify/cors'), {
  origin: process.env.FRONTEND_URL || 'http://localhost:3000'
});

fastify.register(require('@fastify/jwt'), {
  secret: process.env.JWT_SECRET || 'nutrikal-super-secret-key'
});

// Routes
fastify.register(require('./routes/users'), { prefix: '/api/users' });
fastify.register(require('./routes/mealplans'), { prefix: '/api/mealplans' });
fastify.register(require('./routes/scores'), { prefix: '/api/scores' });

// Route de santé
fastify.get('/health', async (request, reply) => {
  return { status: 'healthy', service: 'NUTRIKAL API', timestamp: new Date().toISOString() };
});

// Démarrer serveur
const start = async () => {
  try {
    const port = process.env.PORT || 3001;
    await fastify.listen({ port, host: '0.0.0.0' });
    console.log(`🚀 NUTRIKAL API démarrée sur le port ${port}`);
  } catch (err) {
    fastify.log.error(err);
    process.exit(1);
  }
};

start();
"""

with open('server.js', 'w') as f:
    f.write(server_js)

# BACKEND - Config database
database_config = """const { createClient } = require('@supabase/supabase-js');

const supabaseUrl = process.env.SUPABASE_URL;
const supabaseServiceKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseServiceKey) {
  throw new Error('Variables d\\'environnement Supabase manquantes');
}

const supabase = createClient(supabaseUrl, supabaseServiceKey);

module.exports = { supabase };
"""

with open('database_config.js', 'w') as f:
    f.write(database_config)

# BACKEND - Routes utilisateurs
users_routes = """const { supabase } = require('../config/database');
const bcrypt = require('bcrypt');

async function userRoutes(fastify, options) {
  
  // Inscription
  fastify.post('/register', async (request, reply) => {
    const { email, password, profile } = request.body;
    
    try {
      const hashedPassword = await bcrypt.hash(password, 10);
      
      const { data: user, error: userError } = await supabase
        .from('users')
        .insert([{ email, password_hash: hashedPassword }])
        .select()
        .single();
        
      if (userError) throw userError;
      
      // Créer le profil utilisateur
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
    } catch (error) {
      reply.code(400).send({ error: error.message });
    }
  });
  
  // Connexion
  fastify.post('/login', async (request, reply) => {
    const { email, password } = request.body;
    
    try {
      const { data: user, error } = await supabase
        .from('users')
        .select('*')
        .eq('email', email)
        .single();
        
      if (error || !user) {
        return reply.code(401).send({ error: 'Identifiants invalides' });
      }
      
      const validPassword = await bcrypt.compare(password, user.password_hash);
      if (!validPassword) {
        return reply.code(401).send({ error: 'Identifiants invalides' });
      }
      
      const token = fastify.jwt.sign({ userId: user.id });
      
      reply.send({
        success: true,
        user: { id: user.id, email: user.email },
        token
      });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Obtenir profil utilisateur
  fastify.get('/profile', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    try {
      const { data: profile, error } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', request.user.userId)
        .single();
        
      if (error) throw error;
      
      reply.send({ profile });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Mettre à jour profil
  fastify.put('/profile', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    try {
      const { data: profile, error } = await supabase
        .from('user_profiles')
        .update(request.body)
        .eq('user_id', request.user.userId)
        .select()
        .single();
        
      if (error) throw error;
      
      reply.send({ profile });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
}

module.exports = userRoutes;
"""

with open('users_routes.js', 'w') as f:
    f.write(users_routes)

print("✅ Backend files créés :")
print("  - backend_package.json")
print("  - server.js")
print("  - database_config.js")
print("  - users_routes.js")