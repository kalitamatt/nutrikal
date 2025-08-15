const { supabase } = require('../config/database');
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
