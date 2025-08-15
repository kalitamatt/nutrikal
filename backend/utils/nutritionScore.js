// backend/utils/nutritionScore.js

/**
 * Calcule le score d'adhérence au plan de repas.
 * @param {Array} consumedMeals - Liste des repas réellement consommés.
 * @param {Object} mealPlan - Objet contenant plan_data (tableau de jours avec repas).
 * @returns {number} Score d’adhérence (0–100).
 */
function calculateAdherenceScore(consumedMeals, mealPlan) {
  if (!mealPlan?.plan_data?.length) return 0;
  const totalPlanned = mealPlan.plan_data.length * 3; // ex. 3 repas/jour
  const actual = consumedMeals.length;
  return Math.min((actual / totalPlanned) * 100, 100);
}

/**
 * Calcule le score nutritionnel basé sur les totaux de macro et micronutriments.
 * @param {Array} consumedMeals - Liste des repas avec calories, protéines, omega3, magnesium.
 * @param {Object} targets - Objectifs : calories_target, protein_target, omega3_target, magnesium_target.
 * @returns {number} Score nutritionnel global (0–100).
 */
function calculateNutritionScore(consumedMeals, targets) {
  const totals = consumedMeals.reduce((sum, m) => ({
    calories: sum.calories + (m.calories || 0),
    protein:  sum.protein  + (m.protein  || 0),
    omega3:   sum.omega3   + (m.omega3   || 0),
    magnesium:sum.magnesium+ (m.magnesium|| 0),
  }), { calories: 0, protein: 0, omega3: 0, magnesium: 0 });

  // Calcul des sous-scores (chaque sous-score limité entre 0 et 100)
  const calcSubScore = (value, target, maxFactor = 1.2) =>
    Math.max(0, Math.min((value / target) * 100, maxFactor * 100));

  const caloriesScore  = calcSubScore(totals.calories, targets.calories_target, 1.2);
  const proteinScore   = calcSubScore(totals.protein,  targets.protein_target, 1.5);
  const omega3Score    = calcSubScore(totals.omega3,   targets.omega3_target, 2);
  const magnesiumScore = calcSubScore(totals.magnesium,targets.magnesium_target, 1.5);

  // Pénalité pour excès trop important de calories (>120%)
  const caloriesPenalty = totals.calories > targets.calories_target * 1.2 ? -10 : 0;

  // Pondérations des nutriments pour performance cérébrale
  const WEIGHTS = {
    calories:  0.2,
    protein:   0.3,
    omega3:    0.3,
    magnesium: 0.2,
  };

  let score = (
    caloriesScore  * WEIGHTS.calories +
    proteinScore   * WEIGHTS.protein  +
    omega3Score    * WEIGHTS.omega3   +
    magnesiumScore * WEIGHTS.magnesium
  ) / 100; // ramène à 0–1

  score = (score * 100) + caloriesPenalty;
  return Math.max(0, Math.min(score, 100));
}

/**
 * Calcule le score global quotidien en combinant adhérence, nutrition et feedback cognitif.
 * @param {Array} consumedMeals - Repas consommés.
 * @param {Object} mealPlan - Plan de repas (plan_data).
 * @param {Object} targets - Objectifs nutritionnels.
 * @param {number} cognitiveFeedback - Auto-évaluation cognitive (1–10).
 * @returns {Object} Détails des différents scores et totaux.
 */
function calculateBrainScore(consumedMeals, mealPlan, targets, cognitiveFeedback = 5) {
  const adherence = calculateAdherenceScore(consumedMeals, mealPlan);
  const nutrition = calculateNutritionScore(consumedMeals, targets);
  const cognitive = Math.max(0, Math.min((cognitiveFeedback / 10) * 100, 100));

  // Pondérations globales
  const GLOBAL_WEIGHTS = {
    adherence: 0.4,
    nutrition: 0.4,
    cognitive: 0.2,
  };

  const dailyScore = 
    adherence * GLOBAL_WEIGHTS.adherence +
    nutrition * GLOBAL_WEIGHTS.nutrition +
    cognitive * GLOBAL_WEIGHTS.cognitive;

  const details = consumedMeals.reduce((d, m) => ({
    total_calories: d.total_calories + (m.calories || 0),
    total_protein:  d.total_protein  + (m.protein  || 0),
    total_omega3:   d.total_omega3   + (m.omega3   || 0),
    total_magnesium:d.total_magnesium+ (m.magnesium|| 0),
  }), { total_calories: 0, total_protein: 0, total_omega3: 0, total_magnesium: 0 });

  return {
    daily_score:      Math.round(dailyScore * 10) / 10,
    adherence_score:  Math.round(adherence * 10) / 10,
    nutrition_score:  Math.round(nutrition * 10) / 10,
    cognitive_score:  Math.round(cognitive * 10) / 10,
    cognitive_feedback,
    details,
  };
}

module.exports = {
  calculateAdherenceScore,
  calculateNutritionScore,
  calculateBrainScore,
};
