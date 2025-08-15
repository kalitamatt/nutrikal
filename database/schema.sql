-- NUTRIKAL Database Schema
-- Schéma de base de données pour la plateforme de nutrition cérébrale

-- Table des utilisateurs
CREATE TABLE users (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Table des profils utilisateur
CREATE TABLE user_profiles (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  age INTEGER NOT NULL,
  gender VARCHAR(10) CHECK (gender IN ('M', 'F', 'Other')),
  weight DECIMAL(5,2),
  height DECIMAL(5,2),
  activity_level VARCHAR(20) DEFAULT 'moderate',
  allergies TEXT[],
  food_aversions TEXT[],
  dietary_preferences TEXT[],
  brain_goals TEXT[],
  stress_level INTEGER CHECK (stress_level BETWEEN 1 AND 10),
  sleep_hours DECIMAL(3,1),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Table des objectifs nutritionnels
CREATE TABLE nutrition_targets (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  calories_target DECIMAL(7,2),
  protein_target DECIMAL(6,2),
  omega3_target DECIMAL(5,3),
  magnesium_target DECIMAL(6,2),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table des plans nutritionnels
CREATE TABLE meal_plans (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  plan_name VARCHAR(255),
  plan_data JSONB NOT NULL, -- Stocke le plan 7 jours complet
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table des repas consommés (tracking réel)
CREATE TABLE consumed_meals (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  meal_date DATE NOT NULL,
  meal_type VARCHAR(20) CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
  food_items JSONB NOT NULL, -- Liste des aliments consommés
  calories DECIMAL(7,2),
  protein DECIMAL(6,2),
  omega3 DECIMAL(5,3),
  magnesium DECIMAL(6,2),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Table des scores de performance cérébrale
CREATE TABLE brain_scores (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  score_date DATE NOT NULL,
  daily_score DECIMAL(4,1) CHECK (daily_score BETWEEN 0 AND 100),
  adherence_score DECIMAL(4,1), -- Respect du plan
  nutrition_score DECIMAL(4,1), -- Qualité nutritionnelle
  cognitive_feedback INTEGER, -- Auto-évaluation utilisateur (1-10)
  details JSONB, -- Détails du calcul
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, score_date)
);

-- Table de la base de connaissances alimentaires
CREATE TABLE food_database (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  food_name VARCHAR(255) NOT NULL,
  calories_per_100g DECIMAL(6,2),
  protein_per_100g DECIMAL(5,2),
  omega3_per_100g DECIMAL(5,3),
  magnesium_per_100g DECIMAL(5,2),
  food_category VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes pour performance
CREATE INDEX idx_user_profiles_user_id ON user_profiles(user_id);
CREATE INDEX idx_meal_plans_user_id ON meal_plans(user_id);
CREATE INDEX idx_consumed_meals_user_date ON consumed_meals(user_id, meal_date);
CREATE INDEX idx_brain_scores_user_date ON brain_scores(user_id, score_date);
CREATE INDEX idx_food_database_name ON food_database(food_name);

-- RLS (Row Level Security) pour Supabase
ALTER TABLE user_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE nutrition_targets ENABLE ROW LEVEL SECURITY;
ALTER TABLE meal_plans ENABLE ROW LEVEL SECURITY;
ALTER TABLE consumed_meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE brain_scores ENABLE ROW LEVEL SECURITY;

-- Politiques RLS
CREATE POLICY "Users can view own profile" ON user_profiles FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own profile" ON user_profiles FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can view own meal plans" ON meal_plans FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view own consumed meals" ON consumed_meals FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can view own scores" ON brain_scores FOR SELECT USING (auth.uid() = user_id);
