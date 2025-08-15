# DEPLOYMENT - Docker Compose
docker_compose = """version: '3.8'

services:
  # Backend API
  nutrikal-backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "3001:3001"
    environment:
      - NODE_ENV=production
      - PORT=3001
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_ROLE_KEY=${SUPABASE_SERVICE_ROLE_KEY}
      - JWT_SECRET=${JWT_SECRET}
      - FRONTEND_URL=http://localhost:3000
    volumes:
      - ./backend:/app
      - /app/node_modules
    restart: unless-stopped
    networks:
      - nutrikal-network

  # Frontend Next.js
  nutrikal-frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_SUPABASE_URL=${SUPABASE_URL}
      - NEXT_PUBLIC_SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
      - NEXT_PUBLIC_API_URL=http://localhost:3001
    volumes:
      - ./frontend:/app
      - /app/node_modules
      - /app/.next
    restart: unless-stopped
    networks:
      - nutrikal-network
    depends_on:
      - nutrikal-backend

  # Jan AI Local
  jan-ai:
    image: janai/jan:latest
    ports:
      - "1337:1337"
    volumes:
      - ./ai/jan_data:/app/jan_data
      - ./ai/jan_config.json:/app/config.json
    environment:
      - API_SERVER_HOST=0.0.0.0
      - API_SERVER_PORT=1337
      - CORS_ENABLED=true
    restart: unless-stopped
    networks:
      - nutrikal-network

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    restart: unless-stopped
    networks:
      - nutrikal-network
    depends_on:
      - nutrikal-frontend
      - nutrikal-backend
      - jan-ai

networks:
  nutrikal-network:
    driver: bridge

volumes:
  jan_data:
    driver: local
"""

with open('docker-compose.yml', 'w') as f:
    f.write(docker_compose)

# DEPLOYMENT - Dockerfile Backend
dockerfile_backend = """FROM node:18-alpine

WORKDIR /app

# Installer les dépendances système
RUN apk add --no-cache python3 make g++

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm ci --only=production && npm cache clean --force

# Copier le code source
COPY . .

# Créer un utilisateur non-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nodejs -u 1001

# Changer la propriété des fichiers
RUN chown -R nodejs:nodejs /app
USER nodejs

# Exposer le port
EXPOSE 3001

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD node -e "require('http').get('http://localhost:3001/health', (res) => { process.exit(res.statusCode === 200 ? 0 : 1) })"

# Commande de démarrage
CMD ["npm", "start"]
"""

with open('Dockerfile.backend', 'w') as f:
    f.write(dockerfile_backend)

# DEPLOYMENT - Dockerfile Frontend  
dockerfile_frontend = """FROM node:18-alpine AS deps

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

FROM node:18-alpine AS builder

WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules

# Construire l'application
RUN npm run build && npm prune --production

FROM node:18-alpine AS runner

WORKDIR /app

ENV NODE_ENV production

# Créer un utilisateur non-root
RUN addgroup -g 1001 -S nodejs
RUN adduser -S nextjs -u 1001

# Copier les fichiers nécessaires
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000

# Vérification de santé
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:3000 || exit 1

CMD ["node", "server.js"]
"""

with open('Dockerfile.frontend', 'w') as f:
    f.write(dockerfile_frontend)

# DEPLOYMENT - Variables d'environnement exemple
env_example = """# NUTRIKAL Environment Variables

# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key

# JWT Secret (generate a strong random string)
JWT_SECRET=your-super-secret-jwt-key-change-this-in-production

# API URLs
NEXT_PUBLIC_API_URL=http://localhost:3001
FRONTEND_URL=http://localhost:3000

# Jan AI Configuration
JAN_API_KEY=nutrikal-api-key-2024
JAN_API_URL=http://localhost:1337

# Database (if using custom DB instead of Supabase)
DATABASE_URL=postgresql://user:password@localhost:5432/nutrikal

# Email Configuration (optional, for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-email-password

# Production settings
NODE_ENV=development
PORT=3001
"""

with open('.env.example', 'w') as f:
    f.write(env_example)

print("✅ Configuration de déploiement créée :")
print("  - docker-compose.yml")
print("  - Dockerfile.backend")  
print("  - Dockerfile.frontend")
print("  - .env.example")