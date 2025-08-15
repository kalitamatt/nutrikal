// Utilitaires pour calculer les scores de performance cérébrale

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
