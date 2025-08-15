# DOCUMENTATION - README Principal
readme_content = """# 🧠 NUTRIKAL
**Plateforme de nutrition cérébrale pour dirigeants**

Optimisez votre performance cérébrale grâce à une nutrition personnalisée basée sur l'IA.

## 🚀 Fonctionnalités

- **Profil personnalisé** : Analyse complète de vos besoins nutritionnels
- **Plans sur mesure** : Génération automatique de plans nutritionnels optimisés
- **IA conversationnelle** : Chat local avec Jan.ai pour le suivi quotidien
- **Scoring intelligent** : Calcul de votre score de performance cérébrale
- **Suivi temporel** : Évolution de vos performances dans le temps
- **Base nutritionnelle** : RAG avec données scientifiques sur les aliments

## 🏗️ Architecture

```
Frontend (Next.js + Chakra UI)
    ↓
Backend API (Node.js + Fastify)
    ↓
Base de données (Supabase/PostgreSQL)
    ↓
IA Locale (Jan.ai + RAG)
```

## 📋 Prérequis

- Node.js 18+
- Docker & Docker Compose
- Compte Supabase (gratuit)
- 4GB RAM minimum pour Jan.ai

## ⚡ Installation rapide

### 1. Cloner et configurer

```bash
git clone https://github.com/your-username/nutrikal.git
cd nutrikal

# Copier la configuration d'environnement
cp .env.example .env
```

### 2. Configurer Supabase

1. Créer un projet sur [supabase.com](https://supabase.com)
2. Exécuter le schéma SQL :
   ```sql
   -- Copier le contenu de database/schema.sql
   -- dans l'éditeur SQL de Supabase
   ```
3. Mettre à jour `.env` avec vos clés Supabase

### 3. Démarrer avec Docker

```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier que tout fonctionne
curl http://localhost:3000  # Frontend
curl http://localhost:3001/health  # Backend API
curl http://localhost:1337  # Jan AI
```

### 4. Initialiser les données

```bash
# Importer la base nutritionnelle
cd ai/
python rag_setup.py
```

## 🎯 Utilisation

1. **Accéder à l'app** : http://localhost:3000
2. **Créer un compte** et compléter votre profil
3. **Générer votre plan** nutritionnel personnalisé
4. **Discuter avec l'IA** pour le suivi quotidien
5. **Suivre vos scores** sur le dashboard

## 📁 Structure du projet

```
nutrikal/
├── frontend/          # Next.js app
│   ├── pages/
│   ├── components/
│   └── lib/
├── backend/           # Node.js API
│   ├── routes/
│   ├── utils/
│   └── config/
├── database/          # SQL schemas
├── ai/               # Jan.ai config & RAG
├── deployment/       # Docker configs
└── docs/            # Documentation
```

## 🔧 Développement

### Backend

```bash
cd backend/
npm install
npm run dev  # Port 3001
```

### Frontend

```bash
cd frontend/
npm install
npm run dev  # Port 3000
```

### Base de données

Les migrations sont dans `database/schema.sql`.
Utilisez Supabase Studio pour les modifications.

## 🤖 Configuration IA

### Jan.ai

- **Config** : `ai/jan_config.json`
- **Prompts** : `ai/system_prompts.json`
- **RAG** : `ai/rag_setup.py`

### Personnaliser les prompts

Éditez `ai/system_prompts.json` pour adapter le comportement de l'IA :

```json
{
  "main_prompt": {
    "content": "Votre prompt personnalisé..."
  }
}
```

## 📊 API Endpoints

### Utilisateurs
- `POST /api/users/register` - Inscription
- `POST /api/users/login` - Connexion
- `GET /api/users/profile` - Profil
- `PUT /api/users/profile` - Mise à jour profil

### Plans nutritionnels
- `POST /api/mealplans/generate` - Générer plan
- `GET /api/mealplans/active` - Plan actif
- `POST /api/mealplans/consumed` - Enregistrer repas

### Scores
- `GET /api/scores` - Historique scores
- `POST /api/scores/calculate` - Calculer score
- `GET /api/scores/stats` - Statistiques

## 🔒 Sécurité

- JWT pour l'authentification
- RLS (Row Level Security) sur Supabase
- Variables d'environnement pour les secrets
- CORS configuré
- Validation des données avec Ajv

## 🚀 Déploiement

### Production

```bash
# Build et déployer
docker-compose -f docker-compose.prod.yml up -d
```

### Variables d'environnement

Configurez ces variables pour la production :

```bash
NODE_ENV=production
SUPABASE_URL=your-production-url
JWT_SECRET=your-super-secret-key
```

## 🧪 Tests

```bash
# Backend
cd backend/ && npm test

# Frontend  
cd frontend/ && npm test

# E2E
npm run test:e2e
```

## 📈 Roadmap

- [ ] Application mobile (React Native)
- [ ] Intégration objets connectés (balance, montre)
- [ ] IA avancée (GPT-4, Claude)
- [ ] Marketplace de recettes
- [ ] Communauté dirigeants
- [ ] Rapports médicaux PDF

## 🤝 Contribution

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit (`git commit -m 'Add some AmazingFeature'`)
4. Push (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📄 License

MIT License - voir [LICENSE](LICENSE) pour plus de détails.

## 💡 Support

- Documentation : [docs/](docs/)
- Issues : [GitHub Issues](https://github.com/your-username/nutrikal/issues)
- Email : contact@nutrikal.com

---

**Développé avec ❤️ pour optimiser la performance cérébrale des dirigeants**
"""

with open('README.md', 'w') as f:
    f.write(readme_content)

# DOCUMENTATION - Guide de setup
setup_guide = """# 🛠️ Guide de Setup NUTRIKAL

Ce guide vous accompagne étape par étape pour déployer NUTRIKAL.

## 📋 Checklist pré-installation

- [ ] Node.js 18+ installé
- [ ] Docker Desktop installé et démarré
- [ ] Compte Supabase créé (gratuit)
- [ ] Éditeur de code (VS Code recommandé)
- [ ] Git installé

## 🚀 Installation complète

### Étape 1 : Préparer l'environnement

```bash
# Cloner le repository
git clone https://github.com/your-username/nutrikal.git
cd nutrikal

# Vérifier les prérequis
node --version  # Doit être >= 18
docker --version
```

### Étape 2 : Configurer Supabase

1. **Créer un projet Supabase**
   - Aller sur [supabase.com](https://supabase.com)
   - "New Project" → Choisir un nom et mot de passe
   - Attendre la création (2-3 minutes)

2. **Récupérer les clés**
   - Project Settings → API
   - Copier `URL` et `anon key`
   - Service Role → Copier `service_role key`

3. **Créer le schéma de base**
   ```bash
   # Dans Supabase Dashboard
   # SQL Editor → New Query
   # Copier le contenu de database/schema.sql
   # Exécuter
   ```

4. **Importer les données de test**
   ```bash
   # Copier le contenu de database/seed_data.sql
   # Exécuter dans SQL Editor
   ```

### Étape 3 : Configuration locale

```bash
# Copier les variables d'environnement
cp .env.example .env

# Éditer .env avec vos clés Supabase
nano .env
```

Compléter `.env` :
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
SUPABASE_ANON_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
JWT_SECRET=your-super-secret-random-string
```

### Étape 4 : Démarrer les services

```bash
# Construire et démarrer tous les containers
docker-compose up --build -d

# Vérifier que tout démarre
docker-compose ps
```

Vous devriez voir :
```
NAME                 STATUS
nutrikal-backend     Up 
nutrikal-frontend    Up
jan-ai               Up
nginx                Up
```

### Étape 5 : Initialiser l'IA

```bash
# Configurer le RAG avec les données nutritionnelles
cd ai/
python rag_setup.py

# Vérifier que Jan.ai répond
curl http://localhost:1337/health
```

### Étape 6 : Tests de fonctionnement

1. **Frontend** : http://localhost:3000
   - Page d'accueil doit s'afficher
   - Tester l'inscription/connexion

2. **Backend API** : http://localhost:3001/health
   - Doit retourner `{"status":"healthy"}`

3. **Jan AI** : http://localhost:1337
   - Interface Jan.ai accessible

4. **Base de données**
   - Vérifier dans Supabase Dashboard
   - Tables créées et données importées

## 🔧 Configuration avancée

### Personnaliser les prompts IA

Éditez `ai/system_prompts.json` :

```json
{
  "main_prompt": {
    "content": "Tu es NUTRIKAL AI, spécialisé en nutrition cérébrale..."
  }
}
```

Redémarrer Jan.ai :
```bash
docker-compose restart jan-ai
```

### Ajouter des aliments

1. **Via l'interface Supabase**
   - Table Editor → `food_database`
   - Insert row

2. **Via script**
   ```bash
   cd ai/
   # Éditer nutrition_kb.csv
   python rag_setup.py  # Re-indexer
   ```

### Configuration HTTPS (production)

1. **Obtenir un certificat SSL**
   ```bash
   # Let's Encrypt
   certbot certonly --webroot -w /var/www/html -d your-domain.com
   ```

2. **Configurer Nginx**
   - Éditer `nginx/nginx.conf`
   - Pointer vers vos certificats

3. **Redémarrer**
   ```bash
   docker-compose restart nginx
   ```

## 🚨 Résolution de problèmes

### Backend ne démarre pas
```bash
# Vérifier les logs
docker-compose logs nutrikal-backend

# Problèmes courants :
# - Variables d'environnement manquantes
# - Supabase inaccessible
# - Port 3001 déjà utilisé
```

### Frontend erreur de build
```bash
# Reconstruire
docker-compose build nutrikal-frontend
docker-compose up nutrikal-frontend

# Vérifier next.config.js
```

### Jan.ai ne répond pas
```bash
# Vérifier les ressources
docker stats

# Jan.ai nécessite au moins 2GB RAM
# Vérifier le modèle dans jan_config.json
```

### Base de données vide
```bash
# Re-exécuter le schéma
# Dans Supabase SQL Editor :
# 1. Copier database/schema.sql
# 2. Exécuter
# 3. Copier database/seed_data.sql  
# 4. Exécuter
```

## 📈 Monitoring

### Logs en temps réel
```bash
# Tous les services
docker-compose logs -f

# Service spécifique
docker-compose logs -f nutrikal-backend
```

### Métriques système
```bash
# Utilisation ressources
docker stats

# Espace disque
docker system df
```

### Health checks
```bash
# Scripts de vérification
curl http://localhost:3000 || echo "Frontend KO"
curl http://localhost:3001/health || echo "Backend KO" 
curl http://localhost:1337 || echo "Jan AI KO"
```

## 🔄 Mises à jour

```bash
# Récupérer les dernières modifications
git pull

# Reconstruire si nécessaire
docker-compose build

# Redémarrer
docker-compose up -d
```

## 💾 Sauvegarde

### Base de données
```bash
# Export depuis Supabase Dashboard
# Settings → Database → Backup
```

### Configuration
```bash
# Sauvegarder les fichiers importants
tar -czf nutrikal-backup.tar.gz .env ai/ nginx/
```

## 🎉 Validation finale

Une fois tout installé, vous devriez pouvoir :

1. ✅ Accéder à l'interface web
2. ✅ Créer un compte utilisateur  
3. ✅ Compléter un profil
4. ✅ Générer un plan nutritionnel
5. ✅ Discuter avec l'IA
6. ✅ Voir les scores sur le dashboard

**Bravo ! NUTRIKAL est opérationnel ! 🎊**
"""

with open('SETUP.md', 'w') as f:
    f.write(setup_guide)

print("✅ Documentation complète créée :")
print("  - README.md")
print("  - SETUP.md")

# Résumé final de tous les fichiers créés
print("\n" + "="*50)
print("🎉 APPLICATION NUTRIKAL COMPLÈTE GÉNÉRÉE")
print("="*50)

all_files = [
    "📁 DATABASE:",
    "  - schema.sql (Schéma PostgreSQL/Supabase)",
    "  - seed_data.sql (Données de démarrage)",
    "",
    "📁 BACKEND (Node.js + Fastify):",
    "  - backend_package.json", 
    "  - server.js (Serveur principal)",
    "  - database_config.js (Configuration Supabase)",
    "  - users_routes.js (API utilisateurs)",
    "  - mealplans_routes.js (API plans nutritionnels)",
    "  - scores_routes.js (API scores)",
    "  - nutritionScore.js (Calculs de performance)",
    "",
    "📁 FRONTEND (Next.js + Chakra UI):",
    "  - frontend_package.json",
    "  - next.config.js",
    "  - supabase_lib.js (Config Supabase)",
    "  - index_page.js (Page d'accueil)",
    "  - ProfileForm.jsx (Formulaire profil)",
    "  - Dashboard.jsx (Tableau de bord)",
    "  - ScoreChart.jsx (Graphique scores)",
    "  - MealPlan.jsx (Affichage plans)",
    "",
    "📁 IA & RAG:",
    "  - system_prompts.json (Prompts pour Jan.ai)",
    "  - jan_config.json (Configuration Jan)",
    "  - rag_setup.py (Setup base nutritionnelle)",
    "",
    "📁 DÉPLOIEMENT:",
    "  - docker-compose.yml (Orchestration)",
    "  - Dockerfile.backend",
    "  - Dockerfile.frontend", 
    "  - .env.example (Variables d'environnement)",
    "",
    "📁 DOCUMENTATION:",
    "  - README.md (Guide principal)",
    "  - SETUP.md (Installation détaillée)",
]

for line in all_files:
    print(line)

print("\n🚀 PRÊT À DÉPLOYER !")
print("1. Configurer Supabase")
print("2. Copier .env.example vers .env")
print("3. docker-compose up --build -d")
print("4. Accéder à http://localhost:3000")
print("\n💡 Voir SETUP.md pour les détails complets")