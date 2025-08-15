# BACKEND - Routes meal plans
mealplans_routes = """const { supabase } = require('../config/database');
const { calculateNutritionScore } = require('../utils/nutritionScore');

async function mealPlanRoutes(fastify, options) {
  
  // Générer un plan nutritionnel
  fastify.post('/generate', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    try {
      // Récupérer le profil utilisateur
      const { data: profile, error: profileError } = await supabase
        .from('user_profiles')
        .select('*')
        .eq('user_id', request.user.userId)
        .single();
        
      if (profileError) throw profileError;
      
      // Récupérer les aliments de la base
      const { data: foods, error: foodsError } = await supabase
        .from('food_database')
        .select('*');
        
      if (foodsError) throw foodsError;
      
      // Filtrer selon allergies et aversions
      const filteredFoods = foods.filter(food => 
        !profile.allergies?.includes(food.food_name) &&
        !profile.food_aversions?.includes(food.food_name)
      );
      
      // Générer plan 7 jours (algorithme simple)
      const weekPlan = generateWeeklyPlan(profile, filteredFoods);
      
      // Sauvegarder le plan
      const { data: savedPlan, error: saveError } = await supabase
        .from('meal_plans')
        .insert([{
          user_id: request.user.userId,
          plan_name: `Plan du ${new Date().toLocaleDateString()}`,
          plan_data: weekPlan,
          is_active: true
        }])
        .select()
        .single();
        
      if (saveError) throw saveError;
      
      reply.send({ plan: savedPlan });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Obtenir le plan actif
  fastify.get('/active', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    try {
      const { data: plan, error } = await supabase
        .from('meal_plans')
        .select('*')
        .eq('user_id', request.user.userId)
        .eq('is_active', true)
        .order('created_at', { ascending: false })
        .limit(1)
        .single();
        
      if (error && error.code !== 'PGRST116') throw error;
      
      reply.send({ plan: plan || null });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Enregistrer un repas consommé
  fastify.post('/consumed', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    const { meal_date, meal_type, food_items } = request.body;
    
    try {
      // Calculer les valeurs nutritionnelles
      const nutrition = calculateMealNutrition(food_items);
      
      const { data: meal, error } = await supabase
        .from('consumed_meals')
        .insert([{
          user_id: request.user.userId,
          meal_date,
          meal_type,
          food_items,
          ...nutrition
        }])
        .select()
        .single();
        
      if (error) throw error;
      
      // Recalculer le score du jour
      await updateDailyScore(request.user.userId, meal_date);
      
      reply.send({ meal });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
}

// Fonction utilitaire pour générer un plan hebdomadaire
function generateWeeklyPlan(profile, foods) {
  const plan = [];
  
  for (let day = 1; day <= 7; day++) {
    const dayPlan = {
      day,
      breakfast: selectMeal(foods, 'breakfast', profile),
      lunch: selectMeal(foods, 'lunch', profile),
      dinner: selectMeal(foods, 'dinner', profile)
    };
    plan.push(dayPlan);
  }
  
  return plan;
}

function selectMeal(foods, mealType, profile) {
  // Algorithme simple de sélection de repas
  // En production, utiliser IA ou algorithme plus sophistiqué
  const proteinSources = foods.filter(f => f.protein_per_100g > 15);
  const vegetables = foods.filter(f => f.food_category === 'Légumes');
  const grains = foods.filter(f => f.food_category === 'Céréales');
  
  const protein = proteinSources[Math.floor(Math.random() * proteinSources.length)];
  const veggie = vegetables[Math.floor(Math.random() * vegetables.length)];
  const grain = grains[Math.floor(Math.random() * grains.length)];
  
  return {
    foods: [protein?.food_name, veggie?.food_name, grain?.food_name].filter(Boolean),
    calories: (protein?.calories_per_100g || 0) + (veggie?.calories_per_100g || 0) + (grain?.calories_per_100g || 0),
    protein: (protein?.protein_per_100g || 0) + (veggie?.protein_per_100g || 0) + (grain?.protein_per_100g || 0),
    omega3: (protein?.omega3_per_100g || 0) + (veggie?.omega3_per_100g || 0) + (grain?.omega3_per_100g || 0),
    magnesium: (protein?.magnesium_per_100g || 0) + (veggie?.magnesium_per_100g || 0) + (grain?.magnesium_per_100g || 0)
  };
}

function calculateMealNutrition(foodItems) {
  // Calcule la nutrition totale d'un repas
  let totalCalories = 0, totalProtein = 0, totalOmega3 = 0, totalMagnesium = 0;
  
  foodItems.forEach(item => {
    const quantity = item.quantity || 100; // grammes
    totalCalories += (item.calories_per_100g * quantity) / 100;
    totalProtein += (item.protein_per_100g * quantity) / 100;
    totalOmega3 += (item.omega3_per_100g * quantity) / 100;
    totalMagnesium += (item.magnesium_per_100g * quantity) / 100;
  });
  
  return {
    calories: totalCalories,
    protein: totalProtein,
    omega3: totalOmega3,
    magnesium: totalMagnesium
  };
}

async function updateDailyScore(userId, date) {
  // Cette fonction sera implémentée dans utils/nutritionScore.js
  // pour calculer et mettre à jour le score quotidien
}

module.exports = mealPlanRoutes;
"""

with open('mealplans_routes.js', 'w') as f:
    f.write(mealplans_routes)

# BACKEND - Routes scores
scores_routes = """const { supabase } = require('../config/database');
const { calculateBrainScore } = require('../utils/nutritionScore');

async function scoresRoutes(fastify, options) {
  
  // Obtenir les scores sur une période
  fastify.get('/', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    const { from_date, to_date } = request.query;
    
    try {
      let query = supabase
        .from('brain_scores')
        .select('*')
        .eq('user_id', request.user.userId)
        .order('score_date', { ascending: true });
        
      if (from_date) query = query.gte('score_date', from_date);
      if (to_date) query = query.lte('score_date', to_date);
      
      const { data: scores, error } = await query;
      
      if (error) throw error;
      
      reply.send({ scores });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Calculer le score d'une date spécifique
  fastify.post('/calculate', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    const { date, cognitive_feedback } = request.body;
    
    try {
      // Récupérer les repas consommés ce jour
      const { data: meals, error: mealsError } = await supabase
        .from('consumed_meals')
        .select('*')
        .eq('user_id', request.user.userId)
        .eq('meal_date', date);
        
      if (mealsError) throw mealsError;
      
      // Récupérer le plan actif
      const { data: plan, error: planError } = await supabase
        .from('meal_plans')
        .select('*')
        .eq('user_id', request.user.userId)
        .eq('is_active', true)
        .single();
        
      if (planError) throw planError;
      
      // Récupérer les objectifs nutritionnels
      const { data: targets, error: targetsError } = await supabase
        .from('nutrition_targets')
        .select('*')
        .eq('user_id', request.user.userId)
        .single();
        
      if (targetsError) throw targetsError;
      
      // Calculer le score
      const scoreData = calculateBrainScore(meals, plan, targets, cognitive_feedback);
      
      // Sauvegarder le score
      const { data: savedScore, error: saveError } = await supabase
        .from('brain_scores')
        .upsert([{
          user_id: request.user.userId,
          score_date: date,
          ...scoreData
        }])
        .select()
        .single();
        
      if (saveError) throw saveError;
      
      reply.send({ score: savedScore });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
  
  // Obtenir statistiques globales
  fastify.get('/stats', {
    preHandler: async (request, reply) => {
      try {
        await request.jwtVerify();
      } catch (err) {
        reply.send(err);
      }
    }
  }, async (request, reply) => {
    try {
      const { data: scores, error } = await supabase
        .from('brain_scores')
        .select('daily_score, score_date')
        .eq('user_id', request.user.userId)
        .order('score_date', { ascending: true });
        
      if (error) throw error;
      
      const stats = {
        average_score: scores.length > 0 ? scores.reduce((sum, s) => sum + s.daily_score, 0) / scores.length : 0,
        best_score: scores.length > 0 ? Math.max(...scores.map(s => s.daily_score)) : 0,
        total_days: scores.length,
        trend: calculateTrend(scores)
      };
      
      reply.send({ stats });
    } catch (error) {
      reply.code(500).send({ error: error.message });
    }
  });
}

function calculateTrend(scores) {
  if (scores.length < 2) return 'stable';
  
  const recent = scores.slice(-7); // 7 derniers jours
  const older = scores.slice(-14, -7); // 7 jours précédents
  
  if (recent.length === 0 || older.length === 0) return 'stable';
  
  const recentAvg = recent.reduce((sum, s) => sum + s.daily_score, 0) / recent.length;
  const olderAvg = older.reduce((sum, s) => sum + s.daily_score, 0) / older.length;
  
  const diff = recentAvg - olderAvg;
  
  if (diff > 5) return 'improving';
  if (diff < -5) return 'declining';
  return 'stable';
}

module.exports = scoresRoutes;
"""

with open('scores_routes.js', 'w') as f:
    f.write(scores_routes)

# BACKEND - Utilitaire calcul de score
nutrition_score = """// Utilitaires pour calculer les scores de performance cérébrale

function calculateBrainScore(consumedMeals, mealPlan, targets, cognitiveFeedback = 5) {
  // Calcul du score d'adhérence au plan
  const adherenceScore = calculateAdherenceScore(consumedMeals, mealPlan);
  
  // Calcul du score nutritionnel
  const nutritionScore = calculateNutritionScore(consumedMeals, targets);
  
  // Score cognitif auto-évalué (1-10 -> 0-100)
  const cognitiveScore = (cognitiveFeedback / 10) * 100;
  
  // Score global pondéré
  const dailyScore = (adherenceScore * 0.4) + (nutritionScore * 0.4) + (cognitiveScore * 0.2);
  
  return {
    daily_score: Math.round(dailyScore * 10) / 10, // Arrondi à 1 décimale
    adherence_score: Math.round(adherenceScore * 10) / 10,
    nutrition_score: Math.round(nutritionScore * 10) / 10,
    cognitive_feedback: cognitiveFeedback,
    details: {
      total_calories: consumedMeals.reduce((sum, m) => sum + (m.calories || 0), 0),
      total_protein: consumedMeals.reduce((sum, m) => sum + (m.protein || 0), 0),
      total_omega3: consumedMeals.reduce((sum, m) => sum + (m.omega3 || 0), 0),
      total_magnesium: consumedMeals.reduce((sum, m) => sum + (m.magnesium || 0), 0)
    }
  };
}

function calculateAdherenceScore(consumedMeals, mealPlan) {
  if (!mealPlan || !mealPlan.plan_data) return 0;
  
  // Logique simplifiée : comparer le nombre de repas prévus vs consommés
  const plannedMeals = mealPlan.plan_data.length * 3; // 7 jours * 3 repas
  const actualMeals = consumedMeals.length;
  
  // Score basé sur le pourcentage de repas suivis
  const adherence = Math.min(actualMeals / plannedMeals, 1) * 100;
  
  return adherence;
}

function calculateNutritionScore(consumedMeals, targets) {
  const totals = consumedMeals.reduce((acc, meal) => ({
    calories: acc.calories + (meal.calories || 0),
    protein: acc.protein + (meal.protein || 0),
    omega3: acc.omega3 + (meal.omega3 || 0),
    magnesium: acc.magnesium + (meal.magnesium || 0)
  }), { calories: 0, protein: 0, omega3: 0, magnesium: 0 });
  
  // Calculer le pourcentage d'atteinte de chaque objectif
  const caloriesScore = Math.min(totals.calories / targets.calories_target, 1.2) * 100; // Max 120%
  const proteinScore = Math.min(totals.protein / targets.protein_target, 1.5) * 100;
  const omega3Score = Math.min(totals.omega3 / targets.omega3_target, 2) * 100;
  const magnesiumScore = Math.min(totals.magnesium / targets.magnesium_target, 1.5) * 100;
  
  // Pénaliser les dépassements excessifs de calories
  const caloriesPenalty = totals.calories > targets.calories_target * 1.2 ? -10 : 0;
  
  // Score pondéré selon l'importance pour le cerveau
  const nutritionScore = (caloriesScore * 0.2) + (proteinScore * 0.3) + (omega3Score * 0.3) + (magnesiumScore * 0.2) + caloriesPenalty;
  
  return Math.max(0, Math.min(100, nutritionScore)); // Borner entre 0 et 100
}

module.exports = {
  calculateBrainScore,
  calculateAdherenceScore,
  calculateNutritionScore
};
"""

with open('nutritionScore.js', 'w') as f:
    f.write(nutrition_score)

print("✅ Routes backend complètes créées :")
print("  - mealplans_routes.js")
print("  - scores_routes.js")
print("  - nutritionScore.js")