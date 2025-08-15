# 🛠️ Guide de Setup NUTRIKAL

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
