// backend/routes/mealplans.js

const fp = require('fastify-plugin');
const { supabase } = require('../config/database');
const {
  calculateNutritionScore,
  calculateBrainScore
} = require('../utils/nutritionScore');

/**
 * Routes pour les plans nutritionnels et repas consommés.
 */
async function mealPlanRoutes(fastify, options) {
  // Générer un plan nutritionnel (protégé)
  fastify.post(
    '/generate',
    { preHandler: fastify.authenticate },
    async (request, reply) => {
      try {
        // Récupérer le profil utilisateur
        const { data: profile, error: profileError } = await supabase
          .from('user_profiles')
          .select('*')
          .eq('user_id', request.user.userId)
          .single();
        if (profileError) throw profileError;

        // Récupérer les aliments et filtrer
        const { data: foods, error: foodsError } = await supabase
          .from('food_database')
          .select('*');
        if (foodsError) throw foodsError;

        const filtered = foods.filter(f =>
          !profile.allergies?.includes(f.food_name) &&
          !profile.food_aversions?.includes(f.food_name)
        );

        // Générer et sauvegarder le plan hebdomadaire
        const weekPlan = generateWeeklyPlan(profile, filtered);
        const { data: savedPlan, error: saveError } = await supabase
          .from('meal_plans')
          .insert([{
            user_id:    request.user.userId,
            plan_name:  `Plan du ${new Date().toLocaleDateString()}`,
            plan_data:  weekPlan,
            is_active:  true
          }])
          .select()
          .single();
        if (saveError) throw saveError;

        reply.send({ plan: savedPlan });
      } catch (err) {
        reply.code(500).send({ error: err.message });
      }
    }
  );

  // Obtenir le plan actif (protégé)
  fastify.get(
    '/active',
    { preHandler: fastify.authenticate },
    async (request, reply) => {
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
      } catch (err) {
        reply.code(500).send({ error: err.message });
      }
    }
  );

  // Enregistrer un repas consommé (protégé)
  fastify.post(
    '/consumed',
    { preHandler: fastify.authenticate },
    async (request, reply) => {
      const { meal_date, meal_type, food_items } = request.body;
      try {
        // Calculer la nutrition du repas
        const nutrition = calculateMealNutrition(food_items);

        // Insérer le repas consommé
        const { data: meal, error } = await supabase
          .from('consumed_meals')
          .insert([{
            user_id:    request.user.userId,
            meal_date,
            meal_type,
            food_items,
            ...nutrition
          }])
          .select()
          .single();
        if (error) throw error;

        // Mettre à jour le score quotidien
        await updateDailyScore(request.user.userId, meal_date);

        reply.send({ meal });
      } catch (err) {
        reply.code(500).send({ error: err.message });
      }
    }
  );
}

//
// Fonctions utilitaires internes
//

/**
 * Génère un plan hebdomadaire simple.
 */
function generateWeeklyPlan(profile, foods) {
  const plan = [];
  for (let day = 1; day <= 7; day++) {
    plan.push({
      day,
      breakfast: selectMeal(foods, profile),
      lunch:     selectMeal(foods, profile),
      dinner:    selectMeal(foods, profile)
    });
  }
  return plan;
}

/**
 * Sélectionne aléatoirement un repas équilibré.
 */
function selectMeal(foods, profile) {
  const prot = foods.filter(f => f.protein_per_100g > 15);
  const veg  = foods.filter(f => f.food_category === 'Légumes');
  const grain= foods.filter(f => f.food_category === 'Céréales');

  const pick = arr => arr[Math.floor(Math.random() * arr.length)];
  const p = pick(prot), v = pick(veg), g = pick(grain);

  return {
    foods: [
      p?.food_name,
      v?.food_name,
      g?.food_name
    ].filter(Boolean),
    calories: (p?.calories_per_100g||0) + (v?.calories_per_100g||0) + (g?.calories_per_100g||0),
    protein:  (p?.protein_per_100g||0)  + (v?.protein_per_100g||0)  + (g?.protein_per_100g||0),
    omega3:   (p?.omega3_per_100g||0)   + (v?.omega3_per_100g||0)   + (g?.omega3_per_100g||0),
    magnesium:(p?.magnesium_per_100g||0)+ (v?.magnesium_per_100g||0)+ (g?.magnesium_per_100g||0)
  };
}

/**
 * Calcule les totaux nutritionnels d’un repas selon la quantité.
 */
function calculateMealNutrition(items) {
  return items.reduce((acc, i) => {
    const qty = i.quantity || 100;
    acc.calories  += (i.calories_per_100g  * qty) / 100;
    acc.protein   += (i.protein_per_100g   * qty) / 100;
    acc.omega3    += (i.omega3_per_100g    * qty) / 100;
    acc.magnesium += (i.magnesium_per_100g * qty) / 100;
    return acc;
  }, { calories: 0, protein: 0, omega3: 0, magnesium: 0 });
}

/**
 * Met à jour le score quotidien dans la table scores.
 */
async function updateDailyScore(userId, date) {
  // Récupérer tous les repas de la date
  const { data: meals = [], error } = await supabase
    .from('consumed_meals')
    .select('calories,protein,omega3,magnesium,meal_date')
    .eq('user_id', userId)
    .eq('meal_date', date);
  if (error) throw error;

  // Récupérer le plan actif et les targets
  const { data: plan } = await supabase
    .from('meal_plans')
    .select('plan_data, targets')
    .eq('user_id', userId)
    .eq('is_active', true)
    .single();

  const brainScore = calculateBrainScore(
    meals,
    plan,
    plan.targets || {}
  );

  // Insérer ou mettre à jour le score
  const { error: upsertError } = await supabase
    .from('scores')
    .upsert([{
      user_id: userId,
      score_date: date,
      ...brainScore
    }], { onConflict: ['user_id','score_date'] });
  if (upsertError) throw upsertError;
}

module.exports = fp(mealPlanRoutes);
